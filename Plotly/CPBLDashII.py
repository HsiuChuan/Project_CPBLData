import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pymysql.cursors
import pandas as pd
from plotly.subplots import make_subplots

pd.options.mode.chained_assignment = None  # default='warn'

mydb = pymysql.connect(host='database-cpbl.ceaykxpwwbjr.ap-northeast-1.rds.amazonaws.com',
                       user='admin',
                       passwd='',
                       db='',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# countstartlines
cursorcsl = mydb.cursor()
team_sql = "SELECT * FROM countstartlines"
teams = cursorcsl.execute(team_sql)
teams = cursorcsl.fetchall()
field_names = [i[0] for i in cursorcsl.description]
dfcsl = pd.DataFrame(teams, columns=field_names)

# staticsscore
cursorss = mydb.cursor()
team_sql = "SELECT * FROM staticsscore"
teams = cursorss.execute(team_sql)
teams = cursorss.fetchall()
field_names = [i[0] for i in cursorss.description]
dfss = pd.DataFrame(teams, columns=field_names)

# statplayerscore
cursorsps = mydb.cursor()
team_sql = "SELECT * FROM statplayerscore"
teams = cursorsps.execute(team_sql)
teams = cursorsps.fetchall()
field_names = [i[0] for i in cursorsps.description]
dfsps = pd.DataFrame(teams, columns=field_names)

# winningratio
cursorwr = mydb.cursor()
team_sql = "SELECT * FROM winningratio"
teams = cursorwr.execute(team_sql)
teams = cursorwr.fetchall()
field_names = [i[0] for i in cursorwr.description]
dfwr = pd.DataFrame(teams, columns=field_names)

# winningstartlines
cursorwsl = mydb.cursor()
team_sql = "SELECT * FROM winningstartlines"
teams = cursorwsl.execute(team_sql)
teams = cursorwsl.fetchall()
field_names = [i[0] for i in cursorwsl.description]
dfwsl = pd.DataFrame(teams, columns=field_names)



cursor = mydb.cursor()
cursor2 = mydb.cursor()

# ===========================================================================================
# Create an app with themes
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("CPBL Startline Data",
                        className='text-center bg-white mb-4'),
                width=12)
    ),
    # Single Player Data

    dbc.Row(
        dbc.Col(html.H3("Batting Scores Data",
                        className='text-left mb-4'),
                width=12)
    ),

    # Batting Score Data Dropdown
    dbc.Row([
        dbc.Col([

            dcc.Dropdown(id='Batting-dpdn', placeholder="Select Batting",
                         options=[{'label': x, 'value': x}
                                  for x in ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th']]
                         )
            ,
            dcc.Dropdown(id='Batting Times Ranking-dpdn', placeholder="Select Top Numbers",
                         options=[{'label': 'Top ' + str(i) + ' Players', 'value': i}
                                  for i in range(5, 51, 5)]
                         )
            ,
            dcc.Dropdown(id='Batting Ratio-dpdn', placeholder="Select Batting Ratio",
                         options=[{'label': 'Batting Ratio > ' + str(i) + ' %', 'value': int(i)}
                                  for i in range(20, 110, 10)]
                         )
            ,
            dcc.Dropdown(id='Order-dpdn', placeholder="Select Order",
                         options=[
                             {'label': 'Win(%) 擔任先發時球隊勝率', 'value': 'WinRatio'},
                             {'label': 'AVG 打擊率', 'value': 'AVG'},
                             {'label': 'OPS 攻擊指數', 'value': 'OPS'},
                             {'label': 'OBP 上壘率', 'value': 'OBP'},
                             {'label': 'SLG 長打率', 'value': 'SLG'},
                             {'label': 'H 安打數', 'value': 'Total_H'},
                             {'label': 'HR 全壘打數', 'value': 'Total_HR'}]
                         )
        ], width=4)
    ], justify="start", align="start", className="h-50"),


    # Ploting
    dbc.Row(
        dbc.Col(html.H5("Batting Scores Chart",
                        className='text-lg-center mb-4'),
                width=12),
    ),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fig1')
        ], xs=12, sm=12, md=12, lg=6, xl=6
            # width = {'size': 6, 'offset': 0, 'order': 1}
        )
        ,
        dbc.Col([
            dcc.Graph(id='fig2')
        ], xs=12, sm=12, md=12, lg=6, xl=6
            # width={'size':5, 'offset':0, 'order':2}
        )
    ], no_gutters=False, align="center"),




    # Batting Score Data Table
    dbc.Row(
        dbc.Col(html.H5("Batting Scores Table",
                        className='text-lg-center mb-4'),
                width=12),
    ),

    dbc.Row(
        id='Batting_Table', justify="center"
    ),


    # Single Player Data
    dbc.Row(
        dbc.Col(html.H3("Single Player Data",
                        className='text-left mb-4'),
                width=12)
    ),

    # Dropdown For Player Search
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='PlayerSearch-dpdn', placeholder="Select Player")
            ], width=4)
        ], justify="start", align="start", className="h-50"),

    dbc.Row(
        dbc.Col(html.H5("Batting Scores Chart",
                        className='text-lg-center mb-4'),
                width=12),
    ),

    # Making Plots
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fig3'),
            dcc.Slider(id='Sliderfig3',
                       min=1,
                       max=9,
                       step=None,
                       marks={i: '{}'.format(i) for i in range(10)},
                       value=4
                       )
        ], xs=12, sm=12, md=12, lg=6, xl=6
        ),
        dbc.Col([
            dcc.Graph(id='fig4'),
            dcc.Slider(id='Sliderfig4',
                       min=1,
                       max=9,
                       step=None,
                       marks={i: '{}'.format(i) for i in range(10)},
                       value=4
                       )
        ], xs=12, sm=12, md=12, lg=6, xl=6
            # width={'size':5, 'offset':0, 'order':2}
        )
    ], no_gutters=False, align="center"),

    dbc.Row(
        dbc.Col(html.H5("Batting Starting Lineup Times & Winning Times",
                        className='text-lg-center mb-4'),
                width=12),
    ),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fig5')
        ], xs=12, sm=12, md=12, lg=12, xl=12
            # width = {'size': 6, 'offset': 0, 'order': 1}
        )
    ], no_gutters=False, align="center"),

    dbc.Row(
        dbc.Col(html.H5("Batting Order Times & Winning Times Ratio",
                        className='text-lg-center mb-4'),
                width=12)
    ),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fig6')
        ], xs=12, sm=12, md=12, lg=12, xl=12
            # width={'size':5, 'offset':0, 'order':2}
        )
    ], no_gutters=False, align="center"),


])


# ===========================================================================================
@app.callback(
    dash.dependencies.Output('Batting_Table', 'children'),
    [dash.dependencies.Input('Batting-dpdn', 'value'),
     dash.dependencies.Input('Batting Times Ranking-dpdn', 'value'),
     dash.dependencies.Input('Batting Ratio-dpdn', 'value'),
     dash.dependencies.Input('Order-dpdn', 'value')],
)
def update_table(selected_batting, selected_times, selected_ratio, selected_order):
    # get the player names
    dfcsll = dfcsl[['Name', str(selected_batting), str(selected_batting) + '_Ratio']] \
        .sort_values(by=str(selected_batting), ascending=False) \
        .head(selected_times)
    dfcsll = dfcsll[dfcsll[str(selected_batting) + '_Ratio'] > selected_ratio]
    players = [i for i in list(dfcsll['Name'])]

    # # Filter Data From DF
    dfwrr = dfwr[dfwr['Name'].isin(players)]
    dfwrr = dfwrr[dfwrr['Batting'] == int(str(selected_batting)[0])]
    dfwrr = dfwrr.sort_values(by=[str(selected_order)], ascending=False)

    dataF = dfwrr.to_dict('records')
    columnsF = [{"name": i, "id": i } for i in dfwrr.columns]

    return dash_table.DataTable(data=dataF, columns=columnsF,
                                style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ]
                                )


@app.callback(
    dash.dependencies.Output('fig1', 'figure'),
    # dash.dependencies.Output('Batting_Table', 'children'),
    [dash.dependencies.Input('Batting-dpdn', 'value'),
     dash.dependencies.Input('Batting Times Ranking-dpdn', 'value'),
     dash.dependencies.Input('Batting Ratio-dpdn', 'value'),
     dash.dependencies.Input('Order-dpdn', 'value')],
)
def drawfig1(selected_batting, selected_times, selected_ratio, selected_order):
    # get the player names
    dfcsll = dfcsl[['Name', str(selected_batting), str(selected_batting) + '_Ratio']] \
        .sort_values(by=str(selected_batting), ascending=False) \
        .head(selected_times)
    dfcsll = dfcsll[dfcsll[str(selected_batting) + '_Ratio'] > selected_ratio]
    players = [i for i in list(dfcsll['Name'])]

    # # Filter Data From DF
    dfwrr = dfwr[dfwr['Name'].isin(players)]
    dfwrr = dfwrr[dfwrr['Batting'] == int(str(selected_batting)[0])]
    dfwrr = dfwrr.sort_values(by=[str(selected_order)], ascending=False)

    # Plotting
    traces = {}
    for col in ['Total_PA', 'Total_AB', 'Total_H', 'Total_HR']:
        traces['trace_' + col] = go.Scatter(x=dfwrr['Name'], y=dfwrr[col], name=col, line_shape='linear')

    # convert data to form required by plotly
    data = list(traces.values())
    fig = go.Figure(data)
    fig.update_layout(barmode='group', xaxis_tickangle=-45)

    return fig


@app.callback(
    dash.dependencies.Output('fig2', 'figure'),
    # dash.dependencies.Output('Batting_Table', 'children'),
    [dash.dependencies.Input('Batting-dpdn', 'value'),
     dash.dependencies.Input('Batting Times Ranking-dpdn', 'value'),
     dash.dependencies.Input('Batting Ratio-dpdn', 'value'),
     dash.dependencies.Input('Order-dpdn', 'value')],
)
def drawfig1(selected_batting, selected_times, selected_ratio, selected_order):
    # get the player names
    dfcsll = dfcsl[['Name', str(selected_batting), str(selected_batting) + '_Ratio']] \
        .sort_values(by=str(selected_batting), ascending=False) \
        .head(selected_times)
    dfcsll = dfcsll[dfcsll[str(selected_batting) + '_Ratio'] > selected_ratio]
    players = [i for i in list(dfcsll['Name'])]

    # # Filter Data From DF
    dfwrr = dfwr[dfwr['Name'].isin(players)]
    dfwrr = dfwrr[dfwrr['Batting'] == int(str(selected_batting)[0])]
    dfwrr = dfwrr.sort_values(by=[str(selected_order)], ascending=False)

    # Plotting
    traces = {}
    for col in ['AVG', 'OBP', 'SLG', 'OPS']:
        traces['trace_' + col] = go.Scatter(x=dfwrr['Name'], y=dfwrr[col], name=col, line_shape='linear')

    # convert data to form required by plotly
    data = list(traces.values())
    fig = go.Figure(data)
    fig.update_layout(barmode='group', xaxis_tickangle=-45)

    return fig

# ===========================================================================================

@app.callback(
    dash.dependencies.Output("PlayerSearch-dpdn", "options"),
    [dash.dependencies.Input('Batting-dpdn', 'value'),
     dash.dependencies.Input('Batting Times Ranking-dpdn', 'value'),
     dash.dependencies.Input('Batting Ratio-dpdn', 'value')],
)
def set_players_options(selected_batting, selected_times, selected_ratio):
    # get the player names
    dfcsll = dfcsl[['Name', str(selected_batting), str(selected_batting) + '_Ratio']] \
        .sort_values(by=str(selected_batting), ascending=False) \
        .head(selected_times)
    dfcsll = dfcsll[dfcsll[str(selected_batting) + '_Ratio'] > selected_ratio]
    players = [i for i in list(dfcsll['Name'])]

    return [{'label': i, 'value': i} for i in players]

@app.callback(
    dash.dependencies.Output("PlayerSearch-dpdn", "value"),
    [dash.dependencies.Input("PlayerSearch-dpdn", "options")],
)
def set_teams_value(selected_player):
    return selected_player[0]['value']


# ===========================================================================================

@app.callback(
    dash.dependencies.Output("fig3", "figure"),
    [dash.dependencies.Input("PlayerSearch-dpdn", "value"),
     dash.dependencies.Input("Sliderfig3", "value")],

)
def drawfig3(selected_player, selected_bat): # selected_bat
    dfsss = dfss[(dfss['Name'] == selected_player) & (dfss['Batting'] == int(selected_bat))]
    dfsss = dfsss.sort_values(by=['year'], ascending=True)

    # Plotting
    traces = {}
    for col in ['Total_PA', 'Total_AB', 'Total_H', 'Total_HR']:
        traces['trace_' + col] = go.Scatter(x=dfsss['year'], y=dfsss[col], name=col, line_shape='linear')

    # convert data to form required by plotly
    data = list(traces.values())
    fig = go.Figure(data)
    return fig

@app.callback(
    dash.dependencies.Output("fig4", "figure"),
    [dash.dependencies.Input("PlayerSearch-dpdn", "value"),
     dash.dependencies.Input("Sliderfig4", "value")],

)
def drawfig4(selected_player, selected_bat):
    dfsss = dfss[(dfss['Name'] == selected_player) & (dfss['Batting'] == int(selected_bat))]
    dfsss = dfsss.sort_values(by=['year'], ascending=True)

    # Plotting
    traces = {}
    for col in ['AVG', 'OBP', 'SLG', 'OPS']:
        traces['trace_' + col] = go.Scatter(x=dfsss['year'], y=dfsss[col], name=col, line_shape='linear')

    # convert data to form required by plotly
    data = list(traces.values())
    fig = go.Figure(data)
    return fig

# ===========================================================================================
@app.callback(
    dash.dependencies.Output("fig5", "figure"),
    [dash.dependencies.Input("PlayerSearch-dpdn", "value")],
)
def drawfig5(selected_player):
    dfcsll = dfcsl[dfcsl['Name'] == selected_player]
    dfwsll = dfwsl[dfwsl['Name'] == selected_player]

    # Plotting
    x = ['Batting ' + str(i) for i in range(1, 10)]
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=x,
        y=dfcsll.iloc[0, 1:10].to_list(),
        name='Total Start Line Times',
        marker_color='indianred'
        # orientation='h'
    ))

    fig5.add_trace(go.Bar(
        x=x,
        y=dfwsll.iloc[0, 1:10].to_list(),
        name='Total Win Times',
        marker_color='lightsalmon'
        # orientation='h'
    ))
    fig5.update_layout(barmode='group')
    return fig5

@app.callback(
    dash.dependencies.Output("fig6", "figure"),
    [dash.dependencies.Input("PlayerSearch-dpdn", "value")],
)
def drawfig6(selected_player):
    dfcsll = dfcsl[dfcsl['Name'] == selected_player]
    dfwsll = dfwsl[dfwsl['Name'] == selected_player]

    # Plotting
    x = ['Bat ' + str(i) for i in range(1, 10)]

    fig6 = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig6.add_trace(go.Pie(labels=x,
                          values=dfcsll.iloc[0, 1:10].to_list(),
                          name="Start Line Ratio"),
                   1, 1)
    fig6.add_trace(go.Pie(labels=x,
                          values=dfwsll.iloc[0, 1:10].to_list(),
                          name="Winning Ratio"),
                   1, 2)
    fig6.update_traces(hole=.2, hoverinfo="label+percent+name")

    return fig6





if __name__ == '__main__':
    app.run_server(debug=True)
