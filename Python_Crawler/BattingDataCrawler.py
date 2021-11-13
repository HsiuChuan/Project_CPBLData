import pandas as pd
import random
import time


class MatchGameRun:

    def __init__(self, matchDateDF):
        self.matchDateDF = matchDateDF
        self.gameMatchRDF = []

    def waiting(self):
        """
        It takes some time to wait after every request.
        """
        delay_choices = [5, 10, 6, 11]  # 延遲的秒數
        delay = random.choice(delay_choices)  # 隨機選取秒數
        time.sleep(delay)  # 延遲


    def get_match_run(self):
        """
        Read data from URL and get the match run.
        """
        match_table = pd.read_html(self.matchDateDF.iloc[i, -1])  # Read the url
        match_team = match_table[0]
        match_scores = match_table[2]
        self.gameMatchRDF.append({'year': self.matchDateDF.iloc[i, 0][:4],
                             'ID': self.matchDateDF.iloc[i, 1],
                             'AwayTeam': ' '.join(map(str, match_team.columns.tolist())),
                             'HomeTeam': match_team.iloc[0, 0],
                             'Away_Score': match_scores.iloc[0, 0],
                             'Home_Score': match_scores.iloc[1, 0]})
    def match_run_df(self):
        """
        Return game match run DataFrame.
        """
        return pd.DataFrame(self.gameMatchRDF)


class MatchBattingData:

    def __init__(self, matchDateDF):
        self.matchDateDF = matchDateDF

    def waiting(self):
        """
        It need some time to wait after every request.
        """
        delay_choices = [5, 10, 6, 11]  # 延遲的秒數
        delay = random.choice(delay_choices)  # 隨機選取秒數
        time.sleep(delay)  # 延遲

    def get_bat_need(self, away_bat_df):
        """
        Filter the index with P & Total.
        """
        is_PA = away_bat_df.iloc[:, 0].str.contains(',  (', regex=False) | \
                away_bat_df.iloc[:, 0].str.contains('Total', regex=False) | \
                away_bat_df.iloc[:, 0].str.contains(',  P', regex=False)
        away_bat_need = away_bat_df[~is_PA]
        away_bat_need.index = range(len(away_bat_need))
        return away_bat_need

    def get_bat_name(self, away_bat_df):
        """
        Get the name Column after split
        """
        away_bat_name = away_bat_need.iloc[:, 0].str.split(',', 1, expand=True)
        away_bat_name.index = range(len(away_bat_name))
        away_bat_name = away_bat_name.rename(columns={'0': 'Name'}, inplace=False)
        return away_bat_name

    def get_allbatting_data(self, match_team, bat_need, bat_name):
        away_bat_bases = pd.DataFrame({'year': [self.matchDateDF.iloc[i, 0].year] * len(bat_need),
                                       'ID': self.matchDateDF.iloc[i, 1],
                                       'H&A': ['Away'] * len(bat_need),
                                       'Team': [' '.join(map(str, match_team.columns.tolist()))] * len(bat_need),
                                       'Batting': list(range(1, len(bat_name) + 1))})
        return away_bat_bases


if __name__ == '__main__':

    path = 'D:\Dropbox\Work_Code\Project_CPBL\Data\CPBLDATA_All30Years\matchDateCPBL_All.csv'
    matchDateDF = pd.read_csv(path, index_col=0)

    # Get the match data run dataframe
    MGR = MatchGameRun(matchDateDF)
    for i in range(len(matchDateDF)):
        try:
            MGR.waiting()
            MGR.get_match_run()
            print(i)
        except IndexError:
            pass

    GameMatchRAll = MGR.match_run_df()

    # Get the match batting data dataframe
    MBD = MatchBattingData(matchDateDF)

    GameMatchAll_Batting = pd.DataFrame()
    for i in range(len(matchDateDF)):
        try:
            MBD.waiting()
            match_table = pd.read_html(matchDateDF.iloc[i, -1])  # Read the url
            match_team = match_table[0]

            ## Away Team Batting Data
            away_bat_final = match_table[7]
            away_bat_need = pd.DataFrame(MBD.get_bat_need(away_bat_final))
            away_bat_name = pd.DataFrame(MBD.get_bat_name(MBD.get_bat_need(away_bat_final)))
            away_bat_bases = MBD.get_allbatting_data(match_team, away_bat_need, away_bat_name)
            game_match_Batting_L = pd.concat([away_bat_bases, away_bat_name.iloc[:, 0], away_bat_need.iloc[:, 1:]], axis=1)

            ## Home Team Batting Data
            home_bat_final = match_table[8]
            home_bat_need = pd.DataFrame(MBD.get_bat_need(away_bat_final))
            home_bat_name = pd.DataFrame(MBD.get_bat_name(MBD.get_bat_need(away_bat_final)))
            home_bat_bases = MBD.get_allbatting_data(match_team, home_bat_need, home_bat_name)
            game_match_Batting_R = pd.concat([home_bat_bases, home_bat_name.iloc[:, 0], home_bat_need.iloc[:, 1:]], axis=1)

            ## Combine
            game_match_Batting = game_match_Batting_L.append([game_match_Batting_R])
            GameMatchAll_Batting = GameMatchAll_Batting.append([game_match_Batting])

            print(matchDateDF.iloc[i, 1])
        except IndexError:
            pass

    # store the all the data into CSV file
    GameMatchRAll.to_csv(r'D:\Dropbox\Work_Code\Project_CPBL\GameMatch_R_All.csv', index=False, encoding='utf_8_sig')
    GameMatchAll_Batting.to_csv(r'D:\Dropbox\Work_Code\Project_CPBL\Data\GameMatchAll_Batting.csv', index = False, encoding='utf_8_sig')




