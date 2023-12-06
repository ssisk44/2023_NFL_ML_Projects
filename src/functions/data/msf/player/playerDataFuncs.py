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


def getMSFPlayerDataByYearWeek(year:int, week:int):
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/msf/weekly_player_game_logs/"
    filepath = absProjectPath + targetDirectory + str(year) + '/' + str(week) + '.csv'
    df = pd.read_csv(filepath, index_col=False)
    filteredDF = df.loc[df['#Position'].isin(['QB', 'RB', 'FB', 'WR', 'TE'])]
    df = filteredDF.sort_values(by=['#FirstName']).reset_index()
    return df

def getMSFPlayerFromPlayerDF(msfDF, bdbPlayerName, bdbHomeTeamName):
    for i1, msfEntry in msfDF.iterrows():
        msfHomeTeamName = msfEntry["#Home Team City"] + " " + msfEntry['#Home Team Name']
        msfPlayerName = msfEntry['#FirstName'] + " " + msfEntry['#LastName']

        ###### MULTIPLE PLAYERS WITH THE SAME NAME AT QB RB WR TE ON ONE TEAM?

        ### FIRST CHECK: was their name corrected to match in future player data?
        if msfPlayerName == bdbPlayerName and msfHomeTeamName == bdbHomeTeamName:
            return msfEntry

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
        if msfPlayerName == bdbPlayerName and msfHomeTeamName == bdbHomeTeamName:
            return msfEntry

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
        if msfPlayerName == bdbPlayerName and msfHomeTeamName == bdbHomeTeamName:
            return msfEntry

    return None

