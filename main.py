import datetime
import os
import Controllers.scrappingController as ScrappingController
import Controllers.dataProcessingController as DataProcessingController


def main():
    ################################################################################
    ######                                                                    ######
    #  This should be the first code hit when this script is loaded onto a server  #
    ######                                                                    ######
    ################################################################################

    initializeEnvironmentVariables()

    # THIS WILL BE CHANGED BUT FOR NOW DATA SCRAPPING WILL HAPPEN NOW
    beginDataAcquisitionProcesses()


def initializeEnvironmentVariables():
    """initializes certain environment variables"""
    ## time
    # now = datetime.datetime.now()
    # os.environ["CURRENT_SEASON_YEAR"] = str(now.year)

def beginDataAcquisitionProcesses():
    ScrappingController.main()
    DataProcessingController.main()

main()
