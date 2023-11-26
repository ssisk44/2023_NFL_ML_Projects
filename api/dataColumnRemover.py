#********************* SOLUTION TO DATA HEADERS FOR ALL CURRENT DATA AND PIPELINE **********************#
import dotenv
# for file in folder in weekly player_game_logs
# for file in folder in weekly team_game_logs
import pandas as pd
import os

weeklyTeamGameLogsPath = 'C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/data/nfl/weekly_team_game_logs/'
weeklyPlayerGameLogsPath = 'C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/data/nfl/weekly_player_game_logs/'

def cleanDataHeaders(dirpath, season=None, week=None):
    dotenv.load_dotenv()
    currentSeasonYear = int(os.getenv('CURRENT_SEASON_YEAR'))
    lastCompletedWeek = int(os.getenv('CURRENT_SEASON_LAST_COMPLETED_WEEK'))

    for subdir in os.listdir(dirpath):
        subdirPath = dirpath + subdir + '/'
        subdirSeason = int(subdir)
        for file in os.listdir(subdirPath):
            filePath = subdirPath + file
            fileWeek = int(file[:-4])
            if subdirSeason == currentSeasonYear and fileWeek > lastCompletedWeek:
                continue
            df = pd.read_csv(filePath)
            df = df.iloc[: , 1:]
            pd.DataFrame(df).to_csv(filePath, index=False)


# df = pd.read_csv('C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/data/nfl/weekly_team_game_logs/2017/1.csv')
# df = df.iloc[: , 1:]
# pd.DataFrame(df).to_csv("C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/tmp/XD.csv", index=False)

cleanDataHeaders(weeklyPlayerGameLogsPath)