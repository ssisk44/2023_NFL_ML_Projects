import os
import numpy as np
import pandas as pd


def returnAllPlayedGamesForYearRange(yearStart:int, yearEnd:int):
    """ This method returns all main slate for a season range
    - no need to sort by main slate games, all the game data can be used to understand player efficiency since it is contest independent
    """
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    dirPath = 'data/msf/seasonal_games_schedule/'
    fullDirPath = absProjectPath + dirPath

    dfArr = []
    columns = []
    for filename in os.listdir(fullDirPath):
        fullFilepath = fullDirPath + filename
        year = int(filename[:4])
        if yearStart <= year <= yearEnd:
            df = pd.read_csv(fullFilepath, index_col=False)
            columns = df.columns
            df = df.loc[df['#Played Status'] == "COMPLETED"]
            dfArr.append(df.values.tolist())

        else:
            continue

    # merge dfArr arrays
    allDFArrs = []
    for arr in dfArr:
        for entry in arr:
            allDFArrs.append(entry)

    return pd.DataFrame(allDFArrs, columns=columns)

