import logging
import os
import dotenv
from src.functions.data.msf.player.playerDataFuncs import getMSFPlayerDataByYearWeek
from src.functions.data.dfs.bdb.bdbDataRetrievalFuncs import getBDBDFSDHistoricalPlayerResultsByYearAndWeek
from src.functions.nflFuncs import getWeeksInSeason
from src.functions.data.playerIDBridge import playerIDBridgeFuncs

""" The goal of the player ID bridge is to apply BDB DFS results to msf player entries """

def createPlayerIDBridgeRecords():
    ### Read and compile historical results from 2017-2023, filter by contest positions, sort by first name, attach to historical and DK
    dotenv.load_dotenv()
    apiDataYearStart = int(os.getenv("FIRST_API_SEASON_YEAR"))
    apiDataYearEnd = int(os.getenv("CURRENT_SEASON_YEAR"))
    currentLastWeekNum = int(os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK"))

    #set up unfound name data logging
    os.getenv("ABS_PTOJECT_PATH")
    logging.basicConfig(filename=os.getenv("ABS_PROJECT_PATH") + 'logs/bdbtomsfPlayerIDBridge.log', filemode='w', level=logging.DEBUG)
    logging.info(["bdbPlayerName", "bdbPlayerTeamName", "year", "week", "bdbPlayerDKPoints", "bdbPlayerDKSalary", "FOUND_TYPE"])

    #seed playerIDBridgeRecordsMap
    playerIDBridgeRecordsMap = playerIDBridgeFuncs.seedPlayerIDBridgeRecordsMap()

    for year in range(apiDataYearStart, apiDataYearEnd+1):
        totalSeasonWeeks = getWeeksInSeason(year)
        for week in range(1, totalSeasonWeeks+1):
            if year < apiDataYearEnd or (year == apiDataYearEnd and week <= currentLastWeekNum):
                bdbDF = getBDBDFSDHistoricalPlayerResultsByYearAndWeek(year, week)
                msfDF = getMSFPlayerDataByYearWeek(year, week)
                print(str(year), str(week), len(bdbDF), len(msfDF))
                # playerIDMatchRecords = playerIDBridgeFuncs.createPlayerIDBridge(bdbDF, msfDF, year, week)
                #
                # playerIDBridgeRecordsMap[str(year)][str(week)] = playerIDMatchRecords
            #ex. playerBridge [msfGameID, msfPlayerID, Player Name,


    exit('Quit at end of all seasons')


createPlayerIDBridgeRecords()