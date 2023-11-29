import pandas as pd
import os

def getAllHistoricalWeeklyPlayerData(yearStart, yearEnd):
    dfArr = []
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/dfs/historicalDFSPlayerResults/"
    for subdir in os.listdir(absProjectPath + targetDirectory):
        subdirPath = absProjectPath + targetDirectory + subdir + '/'
        for file in os.listdir(subdirPath):
            filePath = subdirPath + file
            df = pd.read_csv(filePath, index_col=False)
            dfArr.append(df)
    df = pd.concat(dfArr)
    return df



