import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tools.utilityFunctions import getScheduleDataForRange

def processScheduleData():
    yearStart = int(os.environ.get("FIRST_SEASON_YEAR"))
    yearEnd = int(os.environ.get("CURRENT_SEASON_YEAR"))
    allSeasonsGameArr = getScheduleDataForRange(yearStart, yearEnd + 1, "RAW")

    # add data
    r = addSeasonYearToEntries(allSeasonsGameArr)

    # remove unplayed games
    r = removeUnplayedGamesFromSchedule(r)

    ### write processed data to final
    header = ['Week #', 'Day', 'Date', 'Time', 'Winning Team', '@', 'Losing Team', 'Link', 'W Score', 'L Score',
              'W Yds', 'W TO', 'L Yds', 'L TO', 'Season Year']
    pd.DataFrame(r).to_csv('data/Processed/NFLScheduleAndResultsProcessed.csv', index=False, header=header)


def addSeasonYearToEntries(arr):
    newArr = []
    for season in arr:
        year = season[0][2][:4]
        for game in season:
            g = list(game)
            g.append(year)
            newArr.append(g)
    return newArr

def removeUnplayedGamesFromSchedule(arr, overloadDay=4, overloadMonth=10):
    newArr = []

    now = datetime.datetime.now()
    year = now.year
    month = now.month

    ### WILL CAUSE ISSUES IF NOT CHANGED
    # used to perform analysis during game days
    if overloadMonth > 0:
        month = overloadMonth
    # used to perform analysis during game days
    day = now.day
    if overloadDay > 0:
        day = overloadDay

    nowDT = datetime.datetime(year, month, day)

    # removes games if they have not been played before the current datetime
    for game in arr:
        gameYear = int(game[2][:4])
        gameMonth = int(game[2][5:7])
        gameDay = int(game[2][8:])
        gameDT = datetime.datetime(gameYear, gameMonth, gameDay)
        if nowDT > gameDT:
            newArr.append(game)

    return newArr
