import os
import dotenv
import pandas as pd

def convertHistoricalDFSXLSXToCSV():
    """ This should ONLY be run when current season DFS data results are updated, requires manual header deletion and
    column formatting after each run """
    dotenv.load_dotenv()
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/dfs/historicalDFSPlayerResults/"
    currentSeasonYear = int(os.getenv('CURRENT_SEASON_YEAR'))
    fullTargetDirPath = absProjectPath + targetDirectory + "xlsx/"
    for filename in os.listdir(fullTargetDirPath):
        filepath = fullTargetDirPath + filename
        if os.path.isfile(filepath):
            fileYear = int(filename[4:8])
            if currentSeasonYear == fileYear:
                # logging.info("Converted Historical BigDataBall NFL DFS Data for Current Season from XLSX TO CSV... MANUAL EDITING REQUIRED)
                df = pd.read_excel(filepath, index_col=False)
                df.to_csv(absProjectPath + targetDirectory + '/csv/' + str(currentSeasonYear) + '.csv', index=False)