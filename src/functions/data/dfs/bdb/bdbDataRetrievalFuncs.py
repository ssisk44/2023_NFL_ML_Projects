import os
import pandas as pd
import dotenv


def getBDBDFSDHistoricalPlayerResultsByYearWeekTeamName(year: int, week: int, teamName:str):
    """ return player output entries by year and week """
    dotenv.load_dotenv()
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/dfs/historicalDFSPlayerResults/csv/"
    df = pd.read_csv(absProjectPath + targetDirectory + str(year) + ".csv", index_col=False)
    df = df.loc[(df["Week"] == week) & (df["Player Team"] == teamName)]
    df = df.loc[df["DK Position"].isin(['QB', 'RB', 'WR', 'TE'])]
    df = df.sort_values(by=['Player Name']).reset_index()
    return df

def getBDBDFSHistoricalTeamDefenseResultsByYearAndWeek(year: int, week: int):
    """ return team defense output entries by year and week """
    dotenv.load_dotenv()
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/dfs/historicalDFSPlayerResults/csv/"
    df = pd.read_csv(absProjectPath + targetDirectory + str(year) + ".csv", index_col=False)
    df = df.loc[df["Week"] == week]
    df = df.loc[df["DK Position"].isin(["DST"])]
    df = df.sort_values(by=['Player Name']).reset_index()
    return df










