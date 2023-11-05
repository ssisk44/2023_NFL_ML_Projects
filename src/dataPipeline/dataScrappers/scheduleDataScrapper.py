from bs4 import BeautifulSoup
import requests
import pandas as pd
from src import constants as Constants
import os
import logging

def scrapeNFLScheduleForRange(yearStart: int, yearEnd: int):
    for year in range(yearStart, yearEnd+1):
        response = requests.get('https://www.pro-football-reference.com/years/' + str(year) + '/games.htm')
        logging.info("Scrapping Schedule Data for:" + str(year))
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

        # remove index line
        schedule = schedule[1:]

        # replace "boxscore" with game link
        for entry in schedule:
            dateString = entry[2].replace("-", "") + '0'
            homeTeamName = entry[4]
            if entry[5] == '@' or entry[5] == 'N':
                # normalize value
                entry[5] = '@'
                homeTeamName = entry[6]
            homeTeamAbbreviation = Constants.teamNameToFranchiseAbbrevMap[homeTeamName].lower()
            link = 'https://www.pro-football-reference.com/boxscores/' + dateString + homeTeamAbbreviation + '.htm'
            entry[7] = link

        header = ['Week #', 'Day', 'Date', 'Time', 'Winning Team', '@', 'Losing Team', 'Link', 'W Score', 'L Score', 'W Yds', 'W TO', 'L Yds', 'L TO']
        projectFilepath = os.getenv("ABS_PROJECT_PATH")
        fileName = projectFilepath + "data/schedule/raw/" + str(year) + "NFLScheduleAndResults.csv"
        pd.DataFrame(schedule).to_csv(fileName, index=False, header=header)