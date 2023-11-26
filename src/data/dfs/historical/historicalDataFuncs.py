import os

import dotenv
import pandas as pd


def convertHistoricalDFSToCSV():
    """ This should ONLY be run when current season DFS data results are updated, requires manual header deletion and
    column formating after each run """

    dotenv.load_dotenv()
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/dfs/historical/"
    currentSeasonYear = os.getenv('CURRENT_SEASON_YEAR')
    fullTargetDirPath = absProjectPath + targetDirectory
    for filename in os.listdir(fullTargetDirPath):
        filepath = fullTargetDirPath + filename
        if os.path.isfile(filepath):
            fileYear = filename[4:8]
            if currentSeasonYear == fileYear:
                # logging.info("Converted Historical BigDataBall NFL DFS Data for Current Season from XLSX TO CSV... MANUAL EDITING REQUIRED)
                df = pd.read_excel(filepath, index_col=False)
                df.to_csv(fullTargetDirPath + '/csv/' + currentSeasonYear + '.csv', index=False)


def consolidateHistoricalNFLDFSRecords():
    None