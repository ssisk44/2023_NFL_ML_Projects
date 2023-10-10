import os
import pandas as pd
import numpy as np
import datetime

def getScheduleDataForRange(yearStart: int, yearEnd: int):
    scheduleDataDir = "data/RAW/Schedules/"
    scheduleDataDirFileList = os.listdir(scheduleDataDir)
    allSeasonsGameArr = []
    for file in scheduleDataDirFileList:
        thisYear = int(file[:4])
        if yearStart <= thisYear <= yearEnd:
            thisSeasonGameArr = pd.read_csv(scheduleDataDir + file).to_numpy()
            allSeasonsGameArr.append(thisSeasonGameArr)
    return allSeasonsGameArr

def getProcessedScheduleData(dateStart, dateEnd):
    scheduleDataFileName = "data/Processed/Schedules/NFLScheduleAndResultsProcessed.csv"
    arr = pd.read_csv(scheduleDataFileName).to_numpy()
    dateStartYear = int(dateStart[0:4])
    dateStartMonth = int(dateStart[5:7])
    dateStartDay = int(dateStart[8:])
    dateEndYear = int(dateEnd[0:4])
    dateEndMonth = int(dateEnd[5:7])
    dateEndDay = int(dateEnd[8:])
    SDT = datetime.datetime(dateStartYear, dateStartMonth, dateStartDay)
    EDT = datetime.datetime(dateEndYear, dateEndMonth, dateEndDay)

    retArr = []
    for entry in arr:
        gameDate = entry[3]
        gameDateYear = int(gameDate[0:4])
        gameDateMonth = int(gameDate[5:7])
        gameDateDay = int(gameDate[8:])
        GDT = datetime.datetime(gameDateYear, gameDateMonth, gameDateDay)
        if SDT <= GDT <= EDT:
            retArr.append(entry)
    return retArr