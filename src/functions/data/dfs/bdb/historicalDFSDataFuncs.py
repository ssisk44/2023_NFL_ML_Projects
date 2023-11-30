import os
import dotenv
import pandas as pd


def convertHistoricalDFSXLSXToCSV():
    """ This should ONLY be run when current season DFS data results are updated, requires manual header deletion and
    column formating after each run """
    dotenv.load_dotenv()
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/dfs/historicalDFSPlayerResults/"
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


def getDFSHistoricalRecordsForSeasonWeek(seasonYear: int, seasonWeek: int):
    df = pd.read_csv("C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/data/dfs/historicalDFSPlayerResults/csv/" + str(seasonYear) + '.csv')
    filteredDF = df[df['Week'] == seasonWeek]
    return filteredDF

def filterDFSHistoricalRecords(df, isDraftKings:bool = True):
    DKSalary = df['DK Salary']
    DKPoints = df['DK Points']
    df['200ptDKReqValue'] = round((DKSalary/50000)*200, 2)
    df['200ptDKEfficiency'] = round(df['DK Points']/df['200ptDKReqValue'], 2)
    df['200ptDKPointEffValue'] = round(DKPoints * df['200ptDKEfficiency'], 2)
    df = pd.DataFrame(df).sort_values(by=['200ptDKPointEffValue'], ascending=False)
    return df

def getDFSHistoricalPlayerRecordsForSeasonWeekRange(seasonYear:int, weekStart:int, weekEnd:int, filters: dict):
    None

def sortDFSHistoricalPlayersByPosition(df):
    filteredPlayerArray = []
    dfArr = df.to_numpy()
    for player in dfArr:
        playerPosition = player[10]
        if playerPosition == positionName:
            filteredPlayerArray.append(player)
        elif positionName == "FLX" and playerPosition in ["RB", "WR", "TE"]:
            filteredPlayerArray.append(player)
    return filteredPlayerArray
