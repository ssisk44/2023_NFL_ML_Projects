import os
import dotenv
import pandas as pd

from src.functions.data.dfs.bdb.bdbDataRetrievalFuncs import getBDBDFSDHistoricalPlayerResultsByYearWeekTeamName
from src.functions.data.msf.game import gameDataFuncs
from src.functions.datetimeFuncs import calculateSeasonYearFromDate
from src.functions.nflFuncs import getWeeksInSeason


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


def getMSFPlayerDataByYearWeekTeamName(year:int, week:int, teamName:str):
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/msf/weekly_player_game_logs/"
    filepath = absProjectPath + targetDirectory + str(year) + '/' + str(week) + '.csv'
    df = pd.read_csv(filepath, index_col=False)
    filteredDF = df.loc[(df["#Team Name"] == teamName) & df['#Position'].isin(['QB', 'RB', 'FB', 'WR', 'TE'])]
    df = filteredDF.sort_values(by=['#FirstName']).reset_index()
    return df

def getMSFPlayerDataByYearWeekGameTeamName(year:int, week:int, teamName:str):
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/msf/weekly_player_game_logs/"
    filepath = absProjectPath + targetDirectory + str(year) + '/' + str(week) + '.csv'
    df = pd.read_csv(filepath, index_col=False)
    filteredDF = df.loc[(df["#Team City"] + " " + df["#Team Name"] == teamName) & df['#Position'].isin(['QB', 'RB', 'FB', 'WR', 'TE'])]
    df = filteredDF.sort_values(by=['#FirstName']).reset_index()
    return df

def getMSFPlayerFromPlayerDF(msfDF, bdbPlayerEntry):
    bdbPlayerName = bdbPlayerEntry['Player Name']
    bdbPlayerTeamName = bdbPlayerEntry["Player Team"]
    isHome = bdbPlayerEntry["Venue Ownership"] == "Home"
    bdbPlayerDKPosition = bdbPlayerEntry['DK Position']
    bdbPlayerDKSalary = bdbPlayerEntry['DK Salary']
    bdbPlayerDKPoints = bdbPlayerEntry['DK Points']
    bdbPlayerID = bdbPlayerEntry["PlayerID"]

    for i1, msfEntry in msfDF.iterrows():
        msfPlayerTeamName = msfEntry["#Team City"] + " " + msfEntry['#Team Name']
        msfPlayerName = msfEntry['#FirstName'] + " " + msfEntry['#LastName']

        ###### MULTIPLE PLAYERS WITH THE SAME NAME AT QB RB WR TE ON ONE TEAM?

        ### FIRST CHECK: was their name corrected to match in future player data?
        if msfPlayerName == bdbPlayerName and msfPlayerTeamName == bdbPlayerTeamName:
            return pd.concat(pd.Series({"uPlayerName": msfEntry}) + bdbPlayerEntry + msfEntry)

        ### NAME TRIMMING
        # 1) make name all lowercase
        msfPlayerName = msfPlayerName.lower()
        bdbPlayerName = bdbPlayerName.lower()

        # 2) remove special characters
        msfPlayerName = msfPlayerName.replace(".", "").replace("'", "").replace("-","")
        bdbPlayerName = bdbPlayerName.replace(".", "").replace("'", "").replace("-","")

        # 3) remove post name identifiers without string matching real names
        splitMSFPlayerName = msfPlayerName.split(" ")
        if splitMSFPlayerName[-1] in ['jr', 'sr', "ii", "iii", "iv", "v"]:
            msfPlayerName = ' '.join(splitMSFPlayerName[:-1])

        splitBDBPlayerName = bdbPlayerName.split(" ")
        if splitBDBPlayerName[-1] in ['jr', 'sr', "ii", "iii", "iv", "v"]:
            bdbPlayerName = ' '.join(splitBDBPlayerName[:-1])

        ### SECOND CHECK: was player alternate name changed in the future
        if msfPlayerName == bdbPlayerName and msfPlayerTeamName == bdbPlayerTeamName:
            return pd.concat(pd.Series({"uPlayerName": msfEntry}) + bdbPlayerEntry + msfEntry)

        # # 4) manual bank of player names to ignore (LBs?)
        # ignoreNameArr = [
        #     'keith smith',
        #     'brian hill',
        #     'derek watt'
        # ]
        # if msfPlayerName in ignoreNameArr:
        #     print(ignoreNameArr, msfPlayerName)
        #     quit()
        #     return 'manual_removal'

        # 5) manual bank of same players with different names
        alternateNamePlayerDict = { # (msf to bdb) msf filtered name to forced id spelling for bdb
            'robbie anderson': "robby anderson",
            'mitchell trubisky': 'mitch trubisky',
            'benjamin watson': 'ben watson',
            'danny vitale': 'dan vitale',
            'phillip walker': "pj walker",
            "chig okonkwo": "chigoziem okonkwo",
            "gabriel davis": "gabe davis",
            'samouri toure': "samori toure",
            'joshua palmer': 'josh palmer',
            "zonovan knight": 'bam knight',
            "elijah mitchell": "eli mitchell",
            "deonte harty": "deonte harris",
            "nick westbrookikhine": 'nick westbrook',
            "olabisi johnson": "bisi johnson",
            "drew ogletree": "andrew ogletree",
        }

        if msfPlayerName in alternateNamePlayerDict.keys(): #give msf record the name
            msfPlayerName = alternateNamePlayerDict[msfPlayerName]

        ### FINAL CHECK
        if msfPlayerName == bdbPlayerName and msfPlayerTeamName == bdbPlayerTeamName:
            return pd.concat(pd.Series({"uPlayerName": msfEntry}) + bdbPlayerEntry + msfEntry)

    return None

def createMSFPlayerDataMapFromAllRecords():
    apiDataYearStart = int(os.getenv("FIRST_API_SEASON_YEAR"))
    apiDataYearEnd = int(os.getenv("CURRENT_SEASON_YEAR"))
    currentLastWeekNum = int(os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK"))
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")

    """
    ***Data Map Requirements***
    training model - create all weeks of msf model entries, only when match found in bdb (salary and fantasy output req)
        1) player maps - msfPlayerMap = [year][week][msfTeamID] = {playerID: playerEntry, ...}, bdbPlayerMap = [year][week][bdbTeamName] = {playerName: playerEntry, ...}
            o Temporals -> for all seasons within week range getBridgedPlayerRecordsBySeasonWeekRangePlayerID()
        2) team map - [year][week] = {teamName: teamEntry, ...}
            o Temporals -> getTeamEntryForYearWeekTeamName(), getPlayerIDsForYearWeekTeamName()
        3) game map - msfGameMap = [year][week] = {gameID: gameEntry, ...}
            o Temporals -> yearWeekGameIDs = msfGameMap[str(year)][str(week)].keys(), getGameEntryByYearWeekGameID(year, week, msfGameID),
            
    predicting from model - create contest week model prediction data from dk entry csv
        1) DKCD to BDB name,teamName bridge
        
        2) player map - [year][week][playerID]
        3) team map - [year][week][gameID][teamID]
        4) game map - [year][week][gameID]
    """
    msfPlayerDataMap = {}
    bdbPlayerDataMap = {}
    allTeamDataMap = {}
    allGameMap = {}


    for year in range(apiDataYearStart, apiDataYearEnd+1):
        totalSeasonWeeks = getWeeksInSeason(year)
        msfPlayerDataMap[str(year)] = {}
        allTeamDataMap[str(year)] = {}
        allGameMap[str(year)] = {}
        for week in range(1, totalSeasonWeeks+1):
            if year < apiDataYearEnd or (year == apiDataYearEnd and week <= currentLastWeekNum):
                msfPlayerDataMap[str(year)][str(week)] = {}
                allTeamDataMap[str(year)][str(week)] = {}
                allGameMap[str(year)][str(week)] = {}
                msfYearWeekGamesRecords = gameDataFuncs.getMSFGameDataByYearWeek(year, week)
                for i, gameEntry in msfYearWeekGamesRecords.iterrows():
                    msfGameID = gameEntry["#Game ID"]
                    homeTeamID = gameEntry["#Home Team ID"]
                    awayTeamID = gameEntry["#Away Team ID"]
                    teamIDs = [homeTeamID, awayTeamID]
                    for index in range(0, len(teamIDs)):
                        # player data
                        msfDF = getMSFPlayerDataByYearWeekGameIDTeamID(year, week, msfGameID, teamIDs[index])
                        msfPlayerDataMap[str(year)][str(week)][str(teamIDs[index])] = {}

                        # team data
                        for i1,playerEntry in msfDF:
                            playerID = msfDF["#Player ID"]
                            msfPlayerDataMap[str(year)][str(week)][str(teamIDs[index])].update({str(playerID): playerEntry})
                            #

                    # game data
                    allGameMap[str(year)][str(week)].update({str(msfGameID): gameEntry})


    return allPlayerDataMap

