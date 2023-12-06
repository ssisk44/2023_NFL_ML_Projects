import os
import pandas as pd
def getMSFGameDataByYearWeek(year:int, week:int):
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
    df = pd.read_csv(absProjectFilepath + "data/msf/seasonal_games_schedule/" + str(year) + ".csv")
    df = df.loc[df["#Game Week"] == week]
    return df