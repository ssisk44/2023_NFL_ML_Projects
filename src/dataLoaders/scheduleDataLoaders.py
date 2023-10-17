import datetime
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv

def getRawScheduleData():
    projectFilepath = os.getenv("ABS_PROJECT_PATH")
    scheduleDataDir = projectFilepath + "data/raw/schedule/"
    scheduleDataDirFileList = os.listdir(scheduleDataDir)
    allSeasonsGameArr = []
    # get all games for each season
    for file in scheduleDataDirFileList:
        thisSeasonGameArr = pd.read_csv(scheduleDataDir + file, index_col=None).to_numpy()
        allSeasonsGameArr.append(thisSeasonGameArr)
    return allSeasonsGameArr

def getFinalScheduleTrainingData(dateStart: str, dateEnd: str):
    load_dotenv()
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
    dateStartYear = int(dateStart[0:4])
    dateStartMonth = int(dateStart[5:7])
    dateStartDay = int(dateStart[8:])
    dateEndYear = int(dateEnd[0:4])
    dateEndMonth = int(dateEnd[5:7])
    dateEndDay = int(dateEnd[8:])
    SDT = datetime.datetime(dateStartYear, dateStartMonth, dateStartDay)
    EDT = datetime.datetime(dateEndYear, dateEndMonth, dateEndDay)

    scheduleDataFileName = absProjectFilepath + "data/final/schedule/NFLScheduleAndResultsProcessed.csv"
    allScheduleData = pd.read_csv(scheduleDataFileName).to_numpy()
    prunedAllScheduleData = []
    for game in allScheduleData:
        gameDate = str(game[23])
        gameDateYear = int(gameDate[0:4])
        gameDateMonth = int(gameDate[5:7])
        gameDateDay = int(gameDate[8:])
        GDT = datetime.datetime(gameDateYear, gameDateMonth, gameDateDay)
        if SDT <= GDT <= EDT:
            prunedAllScheduleData.append(game)

    finalCols = [
        "season", "weekNum", "isDayGame", "isPrimetime", "isPlayoffs", "homeIsWinner", "homeFranchiseInt",
        "homeOffPointsAvg", "homeOffYardsAvg", "homeOffTOAvg", "homeDefPointsAvg", "homeDefYardsAvg",
        "homeDefTOAvg", "awayFranchiseInt", "awayOffPointsAvg", "awayOffYardsAvg", "awayOffTOAvg",
        "awayDefPointsAvg", "awayDefYardsAvg", "awayDefTOAvg", "Home Score", "Away Score", "Score Diff",
        'Game Date', 'homeTeamName', 'awayTeamName', 'homeIsWinner'
    ]
    df = pd.DataFrame(prunedAllScheduleData, index=None, columns=finalCols)
    return prunedAllScheduleData, df