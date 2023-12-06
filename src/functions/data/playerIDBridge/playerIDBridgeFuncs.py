import logging
import math

import dotenv
import pandas as pd
import os
from src.functions.data.msf.player.playerDataFuncs import getMSFPlayerFromPlayerDF


def seedPlayerIDBridgeRecordsMap():
    # build empty data map (season -> playerID -> week entry) *** flawed because weeks are not numbered
    currentSeasonYear = int(os.getenv('CURRENT_SEASON_YEAR'))
    currentSeasonLastWeekCompleted = int(os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK"))
    playerIDBridgeRecordsMap = {}
    for year in range(2017, int(os.getenv("CURRENT_SEASON_YEAR")) + 1):
        ### seed year
        playerIDBridgeRecordsMap[str(year)] = {}

        ### seed map with week
        absProjectPath = os.getenv("ABS_PROJECT_PATH")
        targetDirectory = "data/msf/weekly_player_game_logs/"
        subdirPath = absProjectPath + targetDirectory + str(year) + '/'
        for file in os.listdir(subdirPath):
            # if the game has not been played yet do NOT seed it
            weekNum = int(file[:-4])
            if year == currentSeasonYear and weekNum > currentSeasonLastWeekCompleted:
                continue
            playerIDBridgeRecordsMap[str(year)][str(weekNum)] = []  # seed week

    return playerIDBridgeRecordsMap


def createPlayerIDBridge(bdbDF, msfDF, year, week):
    """ find player entries by season and week and combine output results *** DOES NOT WORK ON TEAM DEFENSES *** """
    allMatchedPlayerRecords = []
    for i1, bdbPlayerEntry in bdbDF.iterrows():
        # process bdb player data
        bdbPlayerName = bdbPlayerEntry['Player Name']
        bdbPlayerTeamName = bdbPlayerEntry["Player Team"]
        bdbHomeTeamName = bdbPlayerEntry["Player Opponent Team"]
        isHome = bdbPlayerEntry["Venue Ownership"] == "Home"
        if isHome:
            bdbHomeTeamName = bdbPlayerEntry['Player Team']
        bdbPlayerDKPosition = bdbPlayerEntry['DK Position']
        bdbPlayerDKSalary = bdbPlayerEntry['DK Salary']
        bdbPlayerDKPoints = bdbPlayerEntry['DK Points']

        if math.isnan(
                bdbPlayerDKSalary):  # dk salary nan... no player record found in msf -> SOLUTION: throw away if salary of nan
            continue

        # get corresponding msf player
        msfPlayerEntryFoundValue = getMSFPlayerFromPlayerDF(msfDF, bdbPlayerName, bdbHomeTeamName)
        if msfPlayerEntryFoundValue is None:  # if player not found is msf
            if bdbPlayerDKPoints == 0.0:  # they did not have a record because they didnt play
                continue
            logging.info([bdbPlayerName, bdbPlayerTeamName, str(year), str(week), str(bdbPlayerDKPoints),
                          str(bdbPlayerDKSalary), "NOT FOUND"])

        elif type(
                msfPlayerEntryFoundValue) == str and msfPlayerEntryFoundValue == "manual_removal":  # player is on the manual skip list
            logging.info([bdbPlayerName, bdbPlayerTeamName, str(year), str(week), str(bdbPlayerDKPoints),
                          str(bdbPlayerDKSalary), "MANUAL REMOVAL"])
            continue

        else:  # pd series data found
            # append bdb data to msf player entry
            msfDataList = msfPlayerEntryFoundValue.to_list()
            msfDataList.append(year)
            msfDataList.append(week)
            msfDataList.append(bdbPlayerName)
            msfDataList.append(bdbPlayerName)
            msfDataList.append(bdbHomeTeamName)
            msfDataList.append(isHome)
            msfDataList.append(bdbPlayerDKPosition)
            msfDataList.append(bdbPlayerDKSalary)
            msfDataList.append(bdbPlayerDKPosition)
            allMatchedPlayerRecords.append(msfDataList)

    return allMatchedPlayerRecords
