import os
import dotenv
from src.routines.allFullPlayerEntryDataObjectsRoutines.mainAllFullPlayerEntryDataObjectsRoutine import mainAllFullPlayerEntryDataObjectsRoutine
from src.routines.dkContestParticipantBridgeRoutines.mainDKContestParticipantBridgeCreationRoutine import createAllYearsPlayerIDBridgeRecordsMap
from src.routines.dkContestParticipantBridgeRoutines.mainDKContestParticipantBridgeCreationRoutine import createAllYearsTeamIDBridgeRecordsMap

import pandas as pd
def mainPlayerEfficiencyFilterModelCreationRoutine():
    """ This routine trains a player week efficiency filter model for a given week """
    #### get all player and team data (player & team dict shape: season -> week -> gameID -> teamID)

    #### if necessary: create new player and team ID bridges
    createAllYearsPlayerIDBridgeRecordsMap()

    #### if necessary: create full player data records for referencing (**not all bdb players in contest have been in prev contests**)

    #### if necessary: update historical game weather data

    #### Create training data by game using playerIDBridge,


    #### get all team data with results
    # allTeamDataMap = createAllYearsTeamIDBridgeRecordsMap()

    #### acquire full (game, team, player, venue, weather) data by game
    #playerDataObjects = mainAllFullPlayerEntryDataObjectsRoutine(6, 16)

    #### verify data integrity

    #### scale data

    #### setup model

    #### train model

    #### analyze model results

    #### save model



mainPlayerEfficiencyFilterModelCreationRoutine()