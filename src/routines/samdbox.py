import logging
import os
import pandas as pd
from src.functions.data.dfs.bdb.bdbDataRetrievalFuncs import getBDBDFSDHistoricalPlayerResultsByYearWeekTeamName
from src.functions.data.msf.game import gameDataFuncs
from src.functions.data.msf.player.playerDataFuncs import getMSFPlayerDataByYearWeekGameTeamName, getMSFPlayerDataByYearWeekTeamName
from src.functions.data.msf.venue import venueDataFuncs
from src.functions.nflFuncs import getWeeksInSeason
from src.routines.dkContestParticipantBridgeRoutines.mainDKContestParticipantBridgeCreationRoutine import generatePlayerIDBridgeForSeasonWeekGameTeam
from src import constants

apiDataYearStart = int(os.getenv("FIRST_API_SEASON_YEAR"))
apiDataYearEnd = int(os.getenv("CURRENT_SEASON_YEAR"))
currentLastWeekNum = int(os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK"))
absProjectFilepath = os.getenv("ABS_PROJECT_PATH")

gDNumericCols = constants.gDNumCols
gDCategoricalCols = constants.gDCatCols

tDNumericCols = constants.tDNumCols
tDCategoricalCols = constants.tDCatCols

pDNumericCols = constants.pDNumCols
pDCategoricalCols = constants.pDCatCols

vDNumericCols = constants.vDNumCols
vDCategoricalCols = constants.vDCatCols

################## v2 #######################
# wDNumericCols = constants.gDNumCols
# wDCategoricalCols = constants.gDCatCols
#
# iDNumericCols = constants.gDNumCols
# iDCategoricalCols = constants.gDCatCols


def getDFDataByColumns(gameEntry, colArr):
    valuesDict = {}
    for colName in colArr:
        valuesDict[colName] = gameEntry[colName]
    return pd.DataFrame([valuesDict])

# print(pd.DataFrame([{1: "1", 2: "2", 3: "3"}]))
# print(getDFDataByColumns([2, 3])
# exit()


def findBDBRecord(msfTeamName, bdbTeamData):
    for i,bdbEntry in bdbTeamData:
        bdbTeamName = bdbEntry["Player Team"]
        if bdbTeamName == msfTeamName:
            return bdbEntry


def bridgeTeamDataEntries(msfTeamData, bdbTeamData, year, week):
    for i,msfEntry in msfTeamData.iterrows():
        msfTeamName = msfEntry["#Team City"] + " " + msfEntry['#Team Name']
        bdbRecord = findBDBRecord(msfTeamName, bdbTeamData)
        df = pd.concat([msfTeamData, bdbRecord])
        return df
    return None


def getMSFTeamEntry(year, week, teamName):
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/msf/weekly_team_game_logs/"
    filepath = absProjectPath + targetDirectory + str(year) + '/' + str(week) + '.csv'
    df = pd.read_csv(filepath, index_col=False)
    df = df.loc[df["#Team Name"] == teamName]
    df = df.sort_values(by=['#Team Name']).reset_index()
    return df


def getBDBTeamEntry(year, week, teamName):
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/dfs/historicalDFSPlayerResults/csv/"
    filepath = absProjectPath + targetDirectory + str(year) + '.csv'
    df = pd.read_csv(filepath, index_col=False)
    df = df.loc[(df['DK Position'] == "DST") & (df["Week"] == week) & (df["Player Name"] == teamName)]
    df = df.sort_values(by=['Player Name']).reset_index()
    return df



def getMSFandBDBTeamEntryByYearWeekTeamName(year, week, teamName):
    msfTeamData = getMSFTeamEntry(year, week, teamName)
    bdbTeamData = getBDBTeamEntry(year, week, teamName)
    combinedTeamEntry = bridgeTeamDataEntries(msfTeamData, bdbTeamData, year, week)
    if combinedTeamEntry == None:
        logging.info([str(year), str(week), teamName, "BDB TEAM NOT BRIDGED/FOUND FOR MSF TEAM"])
    else:
        return combinedTeamEntry


def getTemporalTeamData(temporalArr):
    pass


def createTTEntries(ttData):
    pass


def adjustTemporalColsArr(temporalArr, ttDNumericCols):
    pass


def getTemporalPlayerData(temporazArr):
    pass


def createPTEntries(ptData):
    pass


def createAllSeasonsTrainingData(temporalArr, trainingWeekRangeStart, trainingWeekRangeEnd):
    gameMap, teamMap, playerMap = {}, {}, {}

    allPlayerFinalEntries = []
    allTeamFinalEntries = []

    for year in range(apiDataYearStart, apiDataYearEnd + 1):  # for year
        totalSeasonWeeks = getWeeksInSeason(year)
        gameMap[str(year)] = {}
        teamMap[str(year)] = {}
        playerMap[str(year)] = {}

        for week in range(1, totalSeasonWeeks + 1):  # for week
            if year < apiDataYearEnd or (year == apiDataYearEnd and week <= currentLastWeekNum):  # if week is in all stored data range
                msfYearWeekGamesRecords = gameDataFuncs.getMSFGameDataByYearWeek(year, week)
                gameMap[str(year)][str(week)] = {}
                teamMap[str(year)][str(week)] = {}
                playerMap[str(year)][str(week)] = {}

                for i, gameEntry in msfYearWeekGamesRecords.iterrows():  # for game
                    venueID = gameEntry['#Venue ID']
                    homeTeamName = gameEntry["#Home Team City"] + " " + gameEntry['#Home Team Name']
                    awayTeamName = gameEntry["#Away Team City"] + " " + gameEntry['#Away Team Name']
                    teamNames = [homeTeamName, awayTeamName]
                    print(year, week, teamNames)

                    gDNumValues, gDCatValues, vDNumValues, vDCatValues = None, None, None, None
                    if trainingWeekRangeStart <= week <= trainingWeekRangeEnd:  # build model training entry values
                        gDNumValues = getDFDataByColumns(gameEntry, gDNumericCols)
                        gDCatValues = getDFDataByColumns(gameEntry, gDCategoricalCols)

                        venueEntry = venueDataFuncs.getVenueEntryByID(venueID)
                        vDNumValues = getDFDataByColumns(venueEntry, vDNumericCols)
                        vDCatValues = getDFDataByColumns(venueEntry, vDCategoricalCols)

                        # wDNumValues = getDFDataByColumns(gameEntry, wDNumericCols)
                        # wDCatValues = getDFDataByColumns(gameEntry, wDCategoricalCols)

                    for index in range(0, len(teamNames)):
                        # set up logging
                        logging.basicConfig(filename=os.getenv("ABS_PROJECT_PATH") + 'logs/bdbtomsfTeamIDBridge.log', filemode='w',
                                            level=logging.DEBUG)

                        # add team data to team map
                        teamEntry = getMSFandBDBTeamEntryByYearWeekTeamName(year, week, teamNames[index])
                        teamMap[str(year)][str(week)] = {str(teamNames[index]): teamEntry}
                        playerMap[str(year)][str(week)][str(teamNames[index])] = {}

                        ttDNumValues, ttDCatValues = None, None
                        if trainingWeekRangeStart <= week <= trainingWeekRangeEnd:  # build team DST model training entry
                            ### get team current week + temporal values and columns
                            ttData = getTemporalTeamData(temporalArr)
                            ttEntries = createTTEntries(ttData)
                            print(ttEntries)

                            adjustedttNumCols = adjustTemporalColsArr(temporalArr, tDNumericCols)
                            ttDNumValues = getDFDataByColumns(ttEntries, adjustedttNumCols)

                            adjustedttCatCols = adjustTemporalColsArr(temporalArr, tDCategoricalCols)
                            ttDCatValues = getDFDataByColumns(ttEntries, adjustedttCatCols)

                            ### create final contest team DST entries
                            allNumDataArrArr = [gDNumValues, vDNumValues, ttDNumValues]
                            allNumDataColNameArrArr = [gDNumericCols, vDNumericCols, tDNumericCols]
                            tNumValues = pd.concat(allNumDataArrArr)
                            tNumCols = pd.concat(allNumDataColNameArrArr).to_list()
                            tNumDF = pd.DataFrame(tNumValues, columns=tNumCols, index=None)

                            allCatDataArrArr = [gDCatValues, vDCatValues, ttDCatValues]
                            allCatDataColNameArrArr = [gDCategoricalCols, vDCategoricalCols, tDCategoricalCols]
                            tCatValues = pd.concat(allCatDataArrArr)
                            tCatCols = pd.concat(allCatDataColNameArrArr).to_list()
                            tCatDF = pd.DataFrame(tCatValues, columns=tCatCols, index=None)

                            allTeamFinalEntries.append({'num': tNumDF, "cat": tCatDF})

                        # get all player data for team
                        msfDF = getMSFPlayerDataByYearWeekGameTeamName(year, week, teamNames[index])

                        # bridge year week team players data
                        bdbDF = getBDBDFSDHistoricalPlayerResultsByYearWeekTeamName(year, week, teamNames[index])  # get bdb player data
                        msfDF = getMSFPlayerDataByYearWeekTeamName(year, week, teamNames[index])  # get msf player data
                        playerSeasonWeekTeamMatchRecords = generatePlayerIDBridgeForSeasonWeekGameTeam(bdbDF, msfDF, year, week)

                        for playerBridgedEntry in playerSeasonWeekTeamMatchRecords:  # for bridged player
                            universalPlayerName = playerBridgedEntry["upnID"]
                            playerMap[str(year)][str(week)][str(teamNames[index])].update({str(universalPlayerName): playerBridgedEntry})  # save now, scale later

                            ### build player model training entry
                            if trainingWeekRangeStart <= week <= trainingWeekRangeEnd:
                                ### get player current week + temporal columns and values
                                ptData = getTemporalPlayerData(temporalArr)
                                ptEntries = createPTEntries(ptData)

                                adjustedNumCols = adjustTemporalColsArr(temporalArr, pDNumericCols)
                                ptDNumValues = getDFDataByColumns(ptEntries, adjustedNumCols)

                                adjustedCatCols = adjustTemporalColsArr(temporalArr, pDCategoricalCols)
                                ptDCatValues = getDFDataByColumns(ptEntries, adjustedCatCols)

                                ### INJURY DATA
                                # iDNumCols
                                # iDCatCols

                                ### create final player entry
                                allNumDataArrArr = [gDNumValues, vDNumValues, ttDNumValues, ptDNumValues]
                                allNumDataColNameArrArr = [gDNumericCols, vDNumericCols, tDNumericCols, pDNumericCols]
                                ptNumEntryValues = pd.concat(allNumDataArrArr)
                                ptNumEntryCols = pd.concat(allNumDataColNameArrArr).to_list()
                                pNumDF = pd.DataFrame(ptNumEntryValues, columns=ptNumEntryCols, index=None)

                                allCatDataArrArr = [gDCatValues, vDCatValues, ttDCatValues, ptDCatValues]
                                allCatDataColNameArrArr = [gDCategoricalCols, vDCategoricalCols, tDCategoricalCols, pDCategoricalCols]
                                ptCatEntryValues = pd.concat(allCatDataArrArr)
                                ptCatEntryCols = pd.concat(allCatDataColNameArrArr).to_list()
                                pCatDF = pd.DataFrame(ptCatEntryValues, columns=ptCatEntryCols, index=None)

                                allPlayerFinalEntries.append({'num': pNumDF, "cat": pCatDF})

    return allPlayerFinalEntries, allTeamFinalEntries


allPlayerFinalEntries, allTeamFinalEntries = createAllSeasonsTrainingData([1, 3, 5], 6, 16)
