import os

import dotenv
import pandas as pd

from src.functions.datetimeFuncs import calculateSeasonYearFromDate


# def createTeamDataMap():
#     teamDataMap = {}
#     for year in range(2017, int(os.getenv("CURRENT_SEASON_YEAR")) + 1):
#         ### populate maps with year
#         teamDataMap[str(year)] = {}
#
#         ### compile all team data by year
#         allTeamDataByYearDFArr = []
#         absProjectPath = os.getenv("ABS_PROJECT_PATH")
#         targetDirectory = "data/msf/weekly_team_game_logs/"
#         subdirPath = absProjectPath + targetDirectory + str(year) + '/'
#         for file in os.listdir(subdirPath):
#             # if the game has not been played yet do NOT include it
#             weekNum = int(file[:-4])
#             if year == int(os.getenv('CURRENT_SEASON_YEAR')) and weekNum > int(
#                     os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK")):
#                 continue
#
#             # read file
#             filePath = subdirPath + file
#             df = pd.read_csv(filePath, index_col=False)
#             allTeamDataByYearDFArr.append(df)
#
#         df = pd.concat(allTeamDataByYearDFArr)  # create one df for the whole year
#         allTeamDataForYearArr = df.to_numpy()
#
#         ### assign team data to map
#         for entry in allTeamDataForYearArr:
#             teamID = entry[13]
#             currentLoggedPlayerIds = teamDataMap[str(year)].keys()
#             if str(teamID) in currentLoggedPlayerIds:  # team id already exists, append entry
#                 teamDataMap[str(year)][str(teamID)].append(entry)
#             else:  # team id does not exist for year, add it
#                 teamDataMap[str(year)][str(teamID)] = [entry]
#
#     return teamDataMap

def getMSFTeamDataByYearWeek(year:int, week:int):
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/msf/weekly_team_game_logs/"
    filepath = absProjectPath + targetDirectory + str(year) + '/' + str(week) + '.csv'
    df = pd.read_csv(filepath, index_col=False)
    df = df.sort_values(by=['#Home Team Abbr.']).reset_index()
    return df

def createTeamDataMapBySeasonAndWeek():
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

