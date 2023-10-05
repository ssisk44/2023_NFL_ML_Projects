import datetime
import os
import The_Course.constructionHQ as DataExtraction


def main():
    ################################################################################
    ######                                                                    ######
    #  This should be the first code hit when this script is loaded onto a server  #
    ######                                                                    ######
    ################################################################################

    initializeEnvironmentVariables()

    # THIS WILL BE CHANGED BUT FOR NOW DATA SCRAPPING WILL HAPPEN NOW
    beginCoreDataExtractionProcesses()


def initializeEnvironmentVariables():
    """initializes certain environment variables"""
    # time
    now = datetime.datetime.now()
    os.environ["CURRENT_SEASON_YEAR"] = str(now.year)

def beginCoreDataExtractionProcesses():
    DataExtraction.main()

main()
