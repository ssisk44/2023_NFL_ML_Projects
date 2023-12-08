import os
import dotenv
from src.routines.allFullPlayerEntryDataObjectsRoutines.mainAllFullPlayerEntryDataObjectsRoutine import mainAllFullPlayerEntryDataObjectsRoutine
from src.routines.dkContestParticipantBridgeRoutines.mainDKContestParticipantBridgeCreationRoutine import createAllYearsPlayerIDBridgeRecordsMap
from src.routines.dkContestParticipantBridgeRoutines.mainDKContestParticipantBridgeCreationRoutine import createAllYearsTeamIDBridgeRecordsMap

from src.functions.data.msf.player import  playerDataFuncs

import pandas as pd
def mainContestParticipantFilterModelsCreationRoutine():
    """ This routine trains a set of models for dfs contest participant output efficiency screening """
    #### TODO: (if necessary) update missing game weather data
    #### TODO: (if necessary) update player data with injury status descriptions
    #### TODO: add player homebrew data preprocessing (playerTeamOff%ByCategory), (player injury history: daysSinceLastInjuryListing, lastInjuryStatusListing, currentHealthyStreakGames, daysSinceLastDesignatedIR, totalIRDesignations)
    #### TODO: add team homebrew data preprocessing (team injury report, current healthy off/def players snap% by position, healthy off/def season volume ratio)

    #### create all player data entries for training #TODO: take in homebrew preprocessed player data
    createAllYearsPlayerIDBridgeRecordsMap() # acquire all player data training entries
    None # separate numerical v categorical and scale player data training entries (save scalars)
    None # train contest player efficiency model (save model)



    #### create all team defense entries for training #TODO: take in homebrew preprocessed team data
    None # acquire all team data training entries
    None  # separate numerical v categorical and scale team data training entries (save scalars)
    None  # train contest player efficiency model (save model)




mainPlayerEfficiencyFilterModelCreationRoutine()