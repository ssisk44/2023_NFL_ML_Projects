import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import numpy as np
import time, os


teams_list = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants', 'New York Jets', 'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Football Team']

team_name_dict = {
    1:  {
            2002: "Arizona Cardinals",
            2003: "Arizona Cardinals",
            2004: "Arizona Cardinals",
            2005: "Arizona Cardinals",
            2006: "Arizona Cardinals",
            2007: "Arizona Cardinals",
            2008: "Arizona Cardinals",
            2009: "Arizona Cardinals",
            2010: "Arizona Cardinals",
            2011: "Arizona Cardinals",
            2012: "Arizona Cardinals",
            2013: "Arizona Cardinals",
            2014: "Arizona Cardinals",
            2016: "",
            2017: "",
            2015: "",
            2018: "",
            2019: "",
            2020: "",
            2021: "",
            2022: "",
            2023: ""
        }

}

'''
Oakland Raiders 1995 to 2019
Las Vegas Raiders 2020 ->

San Diego Chargers 1961 to 2016
Los Angeles Chargers 2017 ->

St. Louis Rams 1995 to 2015
Los Angeles Rams 2016 ->


Washington Redskins ---- to 2019
Washington Football Team 2020 to 2021
Washington Commanders 2023 ->
'''

"""
- create a legend for mapping old team names to current teams
    - lets take data since 2002 when the Houston Texans became the last and 32nd team to join the NFL
"""

##### WORKSHOPING #####
def getNFLPlayersScores():
    chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver

    soup_list = []
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    # for loop for each team and week
    driver.get('https://www.pro-football-reference.com/years/2020/week_1.htm')
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 500);")
    e1 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div[1]/div/ul/li[1]/span')
    e2 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div[1]/div/ul/li[1]/div/ul/li[4]/button')
    time.sleep(2)

    action = ActionChains(driver)
    action.move_to_element(e1).perform()
    action.move_to_element(e2).click().perform()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    crude = soup.find('pre', id='csv_games')
    soup_list.append(crude)
    df = pd.DataFrame(soup_list)
    df.to_csv(r'2020NFLWeek1Team1Team2PlayerResults.csv', index=False)
    driver.close()

    df = pd.read_csv('2020NFLScheduleAndResults.csv').to_numpy()
    arr = df[0][2].split('\n')
    arr.remove('')

    newarr = []
    for i in range(0, len(arr)):
        if arr[i][0] != '':
            newarr.append(arr[i].split(','))
    header = newarr[0]
    pd.DataFrame(newarr[1:]).to_csv('2020NFLScheduleAndResults.csv', index=False, header=header)

def calculateTeamRecordByWeekPerSeason():
    # team week record
    records_array = []
    for team in range(0, len(teams_list)):
        records_array.append([])

    for team in range(0, len(records_array)):
        for week in range(0, 18):  # +1 more than weeks for total
            records_array[team].append([])

    for team in range(0, len(records_array)):
        for week in range(0, 18):
            records_array[team][week].append(0)
            records_array[team][week].append(0)
            records_array[team][week].append(0)

    print(len(records_array))
    print(len(records_array[0]))
    print(len(records_array[0][0]))

    print(records_array)

    df = pd.read_csv('2020NFLScheduleAndResults.csv').to_numpy()
    for game in range(0, 256):
        home_team = ''
        away_team = ''
        index_winner = int(teams_list.index(df[game][4]))
        index_loser = int(teams_list.index(df[game][6]))

        if int(df[game][8]) == int(df[game][9]):  # tie
            records_array[index_winner][int(df[game][0]) - 1][2] = records_array[index_winner][int(df[game][0]) - 1][
                                                                       2] + 1
            records_array[index_loser][int(df[game][0]) - 1][2] = records_array[index_loser][int(df[game][0]) - 1][
                                                                      2] + 1

        else:
            records_array[index_winner][int(df[game][0]) - 1][0] = records_array[index_winner][int(df[game][0]) - 1][
                                                                       0] + 1
            records_array[index_loser][int(df[game][0]) - 1][1] = records_array[index_loser][int(df[game][0]) - 1][
                                                                      1] + 1

    print(records_array[0][0][0])
