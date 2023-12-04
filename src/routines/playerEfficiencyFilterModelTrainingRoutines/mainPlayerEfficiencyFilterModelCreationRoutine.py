import os
import dotenv
from src.routines.allFullPlayerEntryDataObjectsRoutines.mainAllFullPlayerEntryDataObjectsRoutine import mainAllFullPlayerEntryDataObjectsRoutine
import pandas as pd
def mainPlayerEfficiencyFilterModelCreationRoutine():
    """ This routine trains a player week efficiency filter model for a given week """
    dotenv.load_dotenv()

    # get all player data object
    playerDataObjects = mainAllFullPlayerEntryDataObjectsRoutine(6, 16)

    # verify data integrity

    # scale data

    # setup model

    # train model

    # analyze model results

    # save model



mainPlayerEfficiencyFilterModelCreationRoutine()