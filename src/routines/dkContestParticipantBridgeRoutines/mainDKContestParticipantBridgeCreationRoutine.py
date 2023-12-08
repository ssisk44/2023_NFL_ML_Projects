from datetime import datetime
from src.functions.data.msf.player.playerDataFuncs import getMSFPlayerDataByYearWeekTeamName
from src.functions.data.msf.team.teamDataFuncs import getMSFTeamDataByYearWeek
from src.functions.data.dfs.bdb.bdbDataRetrievalFuncs import getBDBDFSDHistoricalPlayerResultsByYearWeekTeamName, getBDBDFSHistoricalTeamDefenseResultsByYearAndWeek
from src.functions.nflFuncs import getWeeksInSeason
from src.functions.data.msf.game import gameDataFuncs
import logging
import math
import dotenv
import pandas as pd
import os
from src.functions.data.msf.player.playerDataFuncs import getMSFPlayerFromPlayerDF

""" The goal of the player ID bridge is to apply BDB DFS results to msf player entries """


################################# PLAYER METHODS ############################################


def createAllYearsPlayerIDBridgeRecordsMap():
    ### Read and compile historical results from 2017-2023, filter by contest positions, sort by first name, attach to historical and DK
    dotenv.load_dotenv()
    apiDataYearStart = int(os.getenv("FIRST_API_SEASON_YEAR"))
    apiDataYearEnd = currentSeasonYear = int(os.getenv("CURRENT_SEASON_YEAR"))
    currentLastWeekNum = int(os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK"))
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")

    # set up logging
    logging.basicConfig(filename=os.getenv("ABS_PROJECT_PATH") + 'logs/bdbtomsfPlayerIDBridge.log', filemode='w',
                        level=logging.DEBUG)
    logging.info(
        ["bdbPlayerName", "bdbPlayerTeamName", "year", "week", "bdbPlayerDKPoints", "bdbPlayerDKSalary", "FOUND_TYPE"])

    playerIDBridgeRecordsArr = []
    for year in range(apiDataYearStart, apiDataYearEnd + 1):
        totalSeasonWeeks = getWeeksInSeason(year)
        for week in range(1, totalSeasonWeeks + 1):
            if year < apiDataYearEnd or (year == apiDataYearEnd and week <= currentLastWeekNum):
                # get games by season week gameID
                msfYearWeekGamesRecords = gameDataFuncs.getMSFGameDataByYearWeek(year, week)
                for i, gameEntry in msfYearWeekGamesRecords.iterrows():
                    gameID = gameEntry["#Game ID"]
                    homeTeamAbbrev = gameEntry["#Home Team Abbr."]
                    awayTeamAbbrev = gameEntry["#Away Team Abbr."]
                    homeTeamName = gameEntry["#Home Team City"] + " " + gameEntry['#Home Team Name']
                    awayTeamName = gameEntry["#Away Team City"] + " " + gameEntry['#Away Team Name']
                    teamNames = [homeTeamName, awayTeamName]
                    teamAbbrevs = [homeTeamAbbrev, awayTeamAbbrev]
                    for index in range(0, len(teamAbbrevs)):
                        bdbDF = getBDBDFSDHistoricalPlayerResultsByYearWeekTeamName(year, week,
                                                                                    teamNames[index])  # add team
                        msfDF = getMSFPlayerDataByYearWeekGameIDTeamAbbrev(year, week, gameID, teamAbbrevs[index])
                        playerSeasonWeekTeamMatchRecords = generatePlayerIDBridgeForSeasonWeekGameTeam(bdbDF, msfDF,
                                                                                                       year, week)

                        # append all records array
                        for entry in playerSeasonWeekTeamMatchRecords:
                            playerIDBridgeRecordsArr.append(entry)

    # write data to csv file
    col = ["Year", "Week", "msfGameID", "msfPlayerTeamName", "msfPlayerID", "msfTeamID", "bdbPlayerID",
           "bdbPlayerName", "bdbPlayerTeamName", "isHome", "bdbPlayerDKPosition", "bdbPlayerDKSalary"
           ]
    targetDir = "data/contestParticipantsIDBridge/player/"
    pd.DataFrame(playerIDBridgeRecordsArr, columns=col).to_csv(
        absProjectFilepath + targetDir + "allPlayerIDBridgeRecords.csv", index=False)

    # write playerIDBridge info to log file
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dict_ = {"Season Created": currentSeasonYear, "Week Created": currentLastWeekNum, "Datetime Performed": dt_string}
    pd.DataFrame([dict_], index=None).to_csv(absProjectFilepath + targetDir + "playerIDBridgeLogs.csv", index=False)


def generatePlayerIDBridgeForSeasonWeekGameTeam(bdbDF, msfDF, year, week):
    """ find player entries by season and week and combine output results *** DOES NOT WORK ON TEAM DEFENSES *** """

    allMatchedPlayerRecords = []
    for i1, bdbPlayerEntry in bdbDF.iterrows():  # player entry is season week teamName
        ### process bdb player data
        bdbPlayerName = bdbPlayerEntry['Player Name']
        bdbPlayerTeamName = bdbPlayerEntry["Player Team"]
        isHome = bdbPlayerEntry["Venue Ownership"] == "Home"
        bdbPlayerDKPosition = bdbPlayerEntry['DK Position']
        bdbPlayerDKSalary = bdbPlayerEntry['DK Salary']
        bdbPlayerDKPoints = bdbPlayerEntry['DK Points']
        bdbPlayerID = bdbPlayerEntry["PlayerID"]

        ### get corresponding msf player data from bdb matching values
        playerBridgedEntry = getMSFPlayerFromPlayerDF(msfDF, bdbPlayerEntry)

        ### handle response
        if playerBridgedEntry is None:  # if player not found is msf
            logging.info([bdbPlayerName, bdbPlayerTeamName, str(year), str(week), str(bdbPlayerDKPoints),
                          str(bdbPlayerDKSalary), "MSF PLAYER NOT MATCHED: ???? ???? ???? ????"])

        else:  # create combined data entry
            allMatchedPlayerRecords.append(playerBridgedEntry)

    return allMatchedPlayerRecords


def plzWork():
    ### Read and compile historical results from 2017-2023, filter by contest positions, sort by first name, attach to historical and DK
    dotenv.load_dotenv()
    apiDataYearStart = int(os.getenv("FIRST_API_SEASON_YEAR"))
    apiDataYearEnd = currentSeasonYear = int(os.getenv("CURRENT_SEASON_YEAR"))
    currentLastWeekNum = int(os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK"))
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")

    # set up logging
    logging.basicConfig(filename=os.getenv("ABS_PROJECT_PATH") + 'logs/bdbtomsfPlayerIDBridge.log', filemode='w',
                        level=logging.DEBUG)
    logging.info(
        ["bdbPlayerName", "bdbPlayerTeamName", "year", "week", "bdbPlayerDKPoints", "bdbPlayerDKSalary", "FOUND_TYPE"])

    playerIDBridgeRecordsArr = []
    for year in range(apiDataYearStart, apiDataYearEnd + 1):
        totalSeasonWeeks = getWeeksInSeason(year)  # total season weeks changed during year range

        for week in range(1, totalSeasonWeeks + 1):
            if year < apiDataYearEnd or (
                    year == apiDataYearEnd and week <= currentLastWeekNum):  # not processing current week forward
                msfYearWeekGamesRecords = gameDataFuncs.getMSFGameDataByYearWeek(year, week)  # get games by season week

                for i, gameEntry in msfYearWeekGamesRecords.iterrows():  # for every year week game
                    gameID = gameEntry["#Game ID"]
                    homeTeamAbbrev = gameEntry["#Home Team Abbr."]
                    awayTeamAbbrev = gameEntry["#Away Team Abbr."]
                    homeTeamName = gameEntry["#Home Team City"] + " " + gameEntry['#Home Team Name']
                    awayTeamName = gameEntry["#Away Team City"] + " " + gameEntry['#Away Team Name']
                    teamNames = [homeTeamName, awayTeamName]
                    teamAbbrevs = [homeTeamAbbrev, awayTeamAbbrev]

                    for index in range(0, len(teamAbbrevs)):  # for every year week game teamAbbrev
                        bdbDF = getBDBDFSDHistoricalPlayerResultsByYearWeekTeamName(year, week, teamNames[
                            index])  # get bdb entries for year week teamName
                        msfDF = getMSFPlayerDataByYearWeekGameIDTeamAbbrev(year, week, gameID, teamAbbrevs[
                            index])  # get msf entries by year week gameID teamAbbrev
                        playerSeasonWeekTeamMatchRecords = generatePlayerIDBridgeForSeasonWeekGameTeam(bdbDF, msfDF, year, week)  # match all records for each team game week year

                        # append all records array
                        for entry in playerSeasonWeekTeamMatchRecords:
                            playerIDBridgeRecordsArr.append(entry)

    # # write data to csv file
    # col = ["Year", "Week"] "msfGameID", "msfPlayerTeamName", "msfPlayerID", "msfTeamID", "bdbPlayerID", "bdbPlayerName", "bdbPlayerTeamName", "isHome", "bdbPlayerDKPosition", "bdbPlayerDKSalary"]
    # targetDir = "data/contestParticipantsIDBridge/player/"
    # pd.DataFrame(playerIDBridgeRecordsArr, columns=col).to_csv(
    #     absProjectFilepath + targetDir + "allPlayerIDBridgeRecords.csv", index=False)
    # # write playerIDBridge info to log file
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # dict_ = {"Season Created": currentSeasonYear, "Week Created": currentLastWeekNum, "Datetime Performed": dt_string}
    # pd.DataFrame([dict_], index=None).to_csv(absProjectFilepath + targetDir + "playerIDBridgeLogs.csv", index=False)
