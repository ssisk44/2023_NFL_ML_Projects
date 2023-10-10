from bs4 import BeautifulSoup
import requests
import pandas as pd
from src.teamNaming import teamNameToSportsReferenceAbbreviationMap

def scrapeNFLScheduleForRange(yearStart: int, yearEnd: int):
    for year in range(yearStart, yearEnd+1):
        response = requests.get('https://www.pro-football-reference.com/years/' + str(year) + '/games.htm')
        print("Parsing Schedule Data for: ", year)
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
        pd.DataFrame(schedule).to_csv('data/Raw/Schedules/'+str(year)+'NFLScheduleAndResults.csv', index=False, header=header)