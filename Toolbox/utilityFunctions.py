import os
import pandas as pd
import numpy as np


def getScheduleDataForRange(yearStart: int, yearEnd: int):
    scheduleDataDir = "Data/Raw/Schedules/"
    scheduleDataDirFileList = os.listdir(scheduleDataDir)
    allSeasonsGameArr = []
    for file in scheduleDataDirFileList:
        thisYear = int(file[:4])
        if yearStart <= thisYear <= yearEnd:
            thisSeasonGameArr = pd.read_csv(scheduleDataDir + file).to_numpy()
            allSeasonsGameArr.append(thisSeasonGameArr)
    return allSeasonsGameArr
