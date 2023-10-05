import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
import numpy as np
import time, os
from The_Toolbox.teamNames import teamNameToSportsReferenceAbbreviationMap

def scrapeNFLScheduleForRange(yearStart: int, yearEnd: int):
    chromedriver = Service(r"C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/The_Toolbox/chromedriver.exe")
    for year in range(yearStart, yearEnd+1):
        response = requests.get('https://www.pro-football-reference.com/years/' + str(year) + '/games.htm')
        print("Parsing data for", year)
        ## TO DO: Prevent overriding already existing data by checking for output filenames
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find_all("tr")
        schedule = []
        for tr in range(0, len(table)):
            thisRow = []
            if tr > 0:
                scheduleWeek = table[tr].findAll('th')
                weekNumber = scheduleWeek[0].text
                if weekNumber == "Week" or weekNumber == "":
                    continue
                thisRow.append(scheduleWeek[0].text)

                scheduleData = table[tr].findAll('td')
                for d in scheduleData:
                    thisRow.append(d.text)
            schedule.append(thisRow)

        #remove index line
        schedule = schedule[1:]

        #replace "boxscore" with game link
        for entry in schedule:
            dateString = entry[2].replace("-", "") + '0'
            homeTeamName = entry[4]
            if entry[5] == '@' or entry[5] == 'N':
                homeTeamName = entry[6]
            homeTeamAbbreviation = teamNameToSportsReferenceAbbreviationMap[homeTeamName].lower()
            link = 'https://www.pro-football-reference.com/boxscores/' + dateString + homeTeamAbbreviation + '.htm'
            entry[7] = link

        header = ['Week #', 'Day', 'Date', 'Time', 'Winning Team', '@', 'Losing Team', 'Link', 'W Score', 'L Score', 'W Yds', 'W TO', 'L Yds', 'L TO']
        pd.DataFrame(schedule).to_csv('Data/Schedules/'+str(year)+'NFLScheduleAndResults.csv', index=False, header=header)










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
