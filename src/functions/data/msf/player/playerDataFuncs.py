import os
import dotenv
import pandas as pd
from src.functions.datetimeFuncs import calculateSeasonYearFromDate

def createSeasonWeekPlayerIDDataMap():
    # build empty data map (season -> playerID -> week entry) *** flawed because weeks are not numbered
    dotenv.load_dotenv()
    currentSeasonYear = int(os.getenv('CURRENT_SEASON_YEAR'))
    currentSeasonLastWeekCompleted = int(os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK"))
    playerDataMap = {}
    for year in range(2017, int(os.getenv("CURRENT_SEASON_YEAR")) + 1):
        ### populate year
        playerDataMap[str(year)] = {}

        ### compile all player data by year
        allPlayerDataByYearDFArr = []
        absProjectPath = os.getenv("ABS_PROJECT_PATH")
        targetDirectory = "data/msf/weekly_player_game_logs/"
        subdirPath = absProjectPath + targetDirectory + str(year) + '/'
        for file in os.listdir(subdirPath):
            # if the game has not been played yet do NOT include it
            weekNum = int(file[:-4])
            if year == currentSeasonYear and weekNum > currentSeasonLastWeekCompleted:
                continue
            playerDataMap[str(year)][str(weekNum)] = {}# populate  week

            # read file
            filePath = subdirPath + file
            df = pd.read_csv(filePath, index_col=False)
            df["#Week"] = weekNum
            allPlayerDataByYearDFArr.append(df)

        df = pd.concat(allPlayerDataByYearDFArr)  # create one df for the whole year
        filteredDF = df.loc[
            df['#Position'].isin(['QB', 'RB', 'WR', 'TE'])]  # filter to only offensive contest positions
        allFilteredPlayerDataForYearArr = filteredDF.to_numpy()

        ### assign player data to map
        for entry in allFilteredPlayerDataForYearArr:
            playerID = entry[13]
            entryWeekNum = entry[-1]
            entryYearNum = calculateSeasonYearFromDate(entry[1])

            currentLoggedPlayerIds = playerDataMap[str(entryYearNum)][str(entryWeekNum)].keys()

            if str(playerID) in currentLoggedPlayerIds:  # player id already exists, append entry
                playerDataMap[str(entryYearNum)][str(entryWeekNum)][str(playerID)].append(entry)
            else:  # player id does not exist for year, add it
                playerDataMap[str(entryYearNum)][str(entryWeekNum)][str(playerID)] = [entry]

    return playerDataMap



def getPlayerRecordsForGameID(year:int, week:int, gameID:int):
    """ build empty data map (year -> week -> gameID -> {playerRecords}) """
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/msf/weekly_player_game_logs/"
    filepath = absProjectPath + targetDirectory + str(year) + '/' + str(week) + '.csv'
    df = pd.read_csv(filepath, index_col=False)
    filteredDF = df.loc[df['#Position'].isin(['QB', 'RB', 'WR', 'TE'])]
    df = filteredDF.loc[(filteredDF['#Game ID'] == gameID)].reset_index()
    return df
