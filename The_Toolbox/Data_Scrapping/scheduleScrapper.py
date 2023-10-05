import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import numpy as np
import time, os
#import tensorflow

def getNFLScheduleForRange(yearStart: int, yearEnd: int):
    print("Hello")











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
