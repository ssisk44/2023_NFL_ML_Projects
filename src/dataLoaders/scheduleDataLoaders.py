import datetime
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from src import constants as Constants

def getRawScheduleData():
    load_dotenv()
    projectFilepath = os.getenv("ABS_PROJECT_PATH")
    scheduleDataDir = projectFilepath + "data/schedule/raw/"
    scheduleDataDirFileList = os.listdir(scheduleDataDir)
    allSeasonsGameArr = []
    # get all games for each season
    for file in scheduleDataDirFileList:
        thisSeasonGameArr = pd.read_csv(scheduleDataDir + file, index_col=None).to_numpy()
        allSeasonsGameArr.append(thisSeasonGameArr)
    return allSeasonsGameArr

def formatRawScheduleData(scheduleData):
    formattedData = []
    for season in scheduleData:
        for game in season:
            formattedData.append(game)
    return formattedData

# def filterGameScheduleDataByDateRange(dateStart: str, dateEnd: str):
#     load_dotenv()
#     absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
#     dateStartYear = int(dateStart[0:4])
#     dateStartMonth = int(dateStart[5:7])
#     dateStartDay = int(dateStart[8:])
#     dateEndYear = int(dateEnd[0:4])
#     dateEndMonth = int(dateEnd[5:7])
#     dateEndDay = int(dateEnd[8:])
#     SDT = datetime.datetime(dateStartYear, dateStartMonth, dateStartDay)
#     EDT = datetime.datetime(dateEndYear, dateEndMonth, dateEndDay)
#
#     scheduleDataFileName = absProjectFilepath + "data/schedule/NFL-Historical-Schedule-And-Results.csv"
#     allScheduleData = pd.read_csv(scheduleDataFileName)
#
#     return allScheduleData