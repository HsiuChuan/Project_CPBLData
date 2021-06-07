import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import random

class MatchDateCrawler():

    def __init__(self):
        pass

    def get_gamedate(self, gamedate_url):
        """
        Get the match game date from the URL.
        """
        respNextDate = requests.get(gamedate_url).text
        soup = BeautifulSoup(respNextDate, 'html5lib')
        gameDate = soup.find('div', 'date_pick_bar').text.strip()
        pattern = '\d+/\d+/\d+'
        match = re.search(pattern, gameDate)
        if match is None:
            return gameDate
        else:
            return match.group(0)

    def get_gameid(self, gameid_url):
        """
        Get the match game ID from the URL.
        """
        respNextID = requests.get(gameid_url).text
        soup = BeautifulSoup(respNextID, 'html5lib')
        gameDates = soup.find_all('div', 'vs_info')
        kk = []
        for gameDate in gameDates:
            kk.append(gameDate.text.strip()[:4])
        return (kk)

    def get_nextgame_inputurl(self, first_url):
        """
        Get the next match game URL from the input URL.
        """
        respOri = requests.get(first_url).text
        soup = BeautifulSoup(respOri, 'html5lib')
        kel = soup.find('div', 'arr_right').a['href']
        return kel

    def waiting(self):
        """
        It need to take some time to wait after every request.
        """
        delay_choices = [5, 10, 6, 11]  # 延遲的秒數
        delay = random.choice(delay_choices)  # 隨機選取秒數
        time.sleep(delay)  # 延遲

    def clean_match_date(self, game_match_data):
        """
        Set up a cleaning pipeline for the row dataframe.
        One for matchDate['Date'] and the other for matchDate['ID'].
        """
        matchDate = pd.DataFrame(game_match_data)
        matchDate['Date'] = pd.to_datetime(matchDate['Date'])
        matchDate['ID'] = matchDate['ID'].str.strip('G')
        matchDate['ID'] = matchDate['ID'].astype('int')
        matchDateDF = matchDate.sort_values(['ID'])
        matchDateDF.index = range(len(matchDateDF))

        return matchDateDF

    def adding_url(self, matchDateDF):
        """
        Concat the needed game match box URL for every match
        """
        matchDateDF['url'] = 'http://www.cpbl.com.tw/games/box.html?&game_type=01&game_id=' + matchDateDF['ID'].map(str) + \
                           '&game_date=' + matchDateDF['Date'].dt.date.map(str) + '&date=' + matchDateDF[
                               'Date'].dt.date.map(str) + '&pbyear=' + matchDateDF['Date'].dt.year.map(str)
        matchDateDF = matchDateDF.sort_values('Date')
        matchDateDF.index = range(len(matchDateDF))

        return matchDateDF


if __name__ == '__main__':

    game_match_data = []
    url_ori = 'http://www.cpbl.com.tw'
    url = 'http://www.cpbl.com.tw/games/box.html?&game_type=01&game_id=1&game_date=2021-03-13&date=2021-03-13&pbyear=2021'

    MDC = MatchDateCrawler()

    # Get the initial gameIDs & gameDate
    # One date may contain 1~3 games
    gameIDs = MDC.get_gameid(url)
    gameDate = pd.to_datetime(MDC.get_gamedate(url)).date()
    print(gameIDs)
    for gameID in gameIDs:
        game_match_data.append({'Date': gameDate,
                                'ID': gameID})

    # Get the gameIDs & gameDate
    # from the second game to the latest game before year 2022
    while url != url_ori:
        # Get the next game URL
        nexturl = MDC.get_nextgame_inputurl(url)
        MDC.waiting()

        # Get the game ID
        gameIDs = MDC.get_gameid(url_ori + nexturl)
        print(gameIDs)

        # Get the game date
        gameDate = pd.to_datetime(MDC.get_gamedate(url_ori + nexturl)).date()
        MDC.waiting()

        if gameDate.year < 2022:
            for gameID in gameIDs:
                game_match_data.append({'Date': gameDate,
                                        'ID': gameID})
        else:
            break

        # Get the next game URL.
        url = url_ori + nexturl

    # Clean Date
    matchDateDF = MDC.clean_match_date(game_match_data)

    # Adding complete game box url into DF
    matchDateDF = MDC.adding_url(matchDateDF)

    ##  writing into  file
    matchDateDF.to_csv("D:\Dropbox\Work_Code\Project_CPBL\Data\matchDateCPBL_All.csv", index=True)
