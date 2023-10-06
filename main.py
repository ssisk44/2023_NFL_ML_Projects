import datetime
import os
import controllers.scrappingController as ScrappingController
import controllers.dataManipulationController as DataProcessingController


def main(testDataAcquisition=False, testAnalysis=True):
    ################################################################################
    ######                                                                    ######
    #  This should be the first code hit when this script is loaded onto a server  #
    ######                                                                    ######
    ################################################################################

    ### Note -> find out what time/how long after a game sportsreference uploads game data (scrape at noon everyday?)
    initializeEnvironmentVariables()

    # the BELOW subsequences are currently performed through manual triggers, this will eventually be moved to a cron
    # TODO: Get the simplest version of this app running on a server with self updating crons/logs with text notifications
    if testDataAcquisition:
        completeDataAcquisitionProcesses()

    elif testAnalysis:
        completeAnalysisProcesses()


def initializeEnvironmentVariables():
    """initializes certain environment variables"""
    ## time
    # now = datetime.datetime.now()
    # os.environ["CURRENT_SEASON_YEAR"] = str(now.year)

def completeDataAcquisitionProcesses():
    ScrappingController.main()

    DataProcessingController.main()

    print("Data Acquisition Complete")

def completeAnalysisProcesses():


    print()


main()
