import os
import dotenv
import numpy as np

from src.functions.nflFuncs import getWeeksInSeason
from src.functions.data.msf.schedule import scheduleDataFuncs
from src.functions.data.msf.player import playerDataFuncs
from src.functions.data.msf.team import teamDataFuncs
from src.functions.data.msf.game import gameDataFuncs
#from src.functions.data.msf.injury import injuryDataFuncs
from src.functions.data.msf.venue import venueDataFuncs
from src.functions.data.weather import weatherDataFuncs
from src.functions.data.playerIDBridge import playerIDBridgeFuncs
import pandas as pd
from src import constants
from src.functions.datetimeFuncs import calculateSeasonYearFromDate

def mainAllFullPlayerEntryDataObjectsRoutine(weekStart:int, weekEnd:int, temporalValuesArr=[]):
    """
        DESIGN FOR THIS ROUTINE
        # for game in seasonsEntries
            # if in week range
                # compile game data DONE
                # compile each players data DONE
                # compile each teams data DONE
                # compile venue data
                # compile weather data
                # TODO: compile injury data

                # compile player results
                # get msf to bdb ID bridge

                # make player data entry
        """
    # if temporalValuesArr is None: # set a default value???????
    #     # numbers indicate weeks in past from current weak value to include in week range for value averaging
    #     temporalValuesArr = [0, 1, 2, 3, 5]
    # numTemporals = len(temporalValuesArr) + 1 # used later for header assignment (includes season avg)
    # ### TODO: add whole season until current week value avg?
    #
    # # get all played games in data history

    #
    #
    # ### maps for ease in temporal calculations (allows search through years by player ids, then by week)
    # playerDataMap = playerDataFuncs.createPlayerDataMap()
    # teamDataMap = teamDataFuncs.createTeamDataMap()

    ### maps for ease in season -> week -> player/team relationships
    seasonWeekPlayerIDMap = playerDataFuncs.createSeasonWeekPlayerIDDataMap()
    # gameTeamMap = {}


    allGameEntries = scheduleDataFuncs.returnAllPlayedGamesForYearRange(2017,
                                                                                 int(os.getenv("CURRENT_SEASON_YEAR")))
    allCompletePlayerEntries = []
    # create player entries for games in training week range
    for worthlessIndex1, gameEntry in allGameEntries.iterrows():
        if weekStart <= int(gameEntry["#Game Week"]) <= weekEnd:
            gameID = int(gameEntry["#Game ID"])
            gameSeason = int(calculateSeasonYearFromDate(gameEntry["#Game Date"]))
            gameWeek = int(gameEntry["#Game Week"])
            awayTeamID = int(gameEntry["#Away Team ID"])
            awayTeamTemporalDataResults = []
            homeTeamID = int(gameEntry["#Home Team ID"])
            homeTeamTemporalData = []
            venueID = int(gameEntry["#Venue ID"])

            # get game players by game ID
            gamePlayers = playerDataFuncs.getPlayerRecordsForGameID(int(gameSeason), int(gameWeek), int(gameID))

            ### make each player record
            for worthlessIndex2,playerGameRecord in gamePlayers.iterrows():
                playerID = playerGameRecord[14]

                ### retrieve temporal data for player season week entry (remove byes from average or injury games from pool?)
                playerTemporalEntriesArr = []
                for temporalGameWeek in range(gameWeek, gameWeek-6, -1):
                    # if player ID exists in keys
                    if str(playerID) in seasonWeekPlayerIDMap[str(gameSeason)][str(temporalGameWeek)].keys():
                        playerSeasonWeekEntry = seasonWeekPlayerIDMap[str(gameSeason)][str(temporalGameWeek)][str(playerID)]
                        playerTemporalEntriesArr.append(playerSeasonWeekEntry)
                    else:
                        None
                        ### is it a bye week? insert season avgs
                        ### else put in 0s
                        # playerTemporalEntriesArr.append(np.concatenate([np.zeros(174), temporalGameWeek], axis=0))

                ### retrieve player career averages?

                ### create player temporals

                # get player opp team previous week range records
                # create player opp team temporals (remove byes from averaging pool)

                # get player opp team previous week range records
                # create player opp team temporals (remove byes from averaging pool)

                # get venue data (add covering, turf type, and long/lat data)
                # get game weather data (add weather data from venue long/lat to games)
                # create msf to bdb ID bridge (create bridge)
                # get player bdb output for week (create retrieval functions)
                # create and append player week entry
                ### final return should be: concat[[game,venue,weather,player,#injuryHistory,playerTeam,opponentTeam,results]

                exit()










