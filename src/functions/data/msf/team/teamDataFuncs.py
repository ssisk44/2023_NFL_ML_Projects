import os
import pandas as pd

def createTeamDataMap():
    teamDataMap = {}
    for year in range(2017, int(os.getenv("CURRENT_SEASON_YEAR")) + 1):
        ### populate maps with year
        teamDataMap[str(year)] = {}

        ### compile all team data by year
        allTeamDataByYearDFArr = []
        absProjectPath = os.getenv("ABS_PROJECT_PATH")
        targetDirectory = "data/msf/weekly_team_game_logs/"
        subdirPath = absProjectPath + targetDirectory + str(year) + '/'
        for file in os.listdir(subdirPath):
            # if the game has not been played yet do NOT include it
            weekNum = int(file[:-4])
            if year == int(os.getenv('CURRENT_SEASON_YEAR')) and weekNum > int(
                    os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK")):
                continue

            # read file
            filePath = subdirPath + file
            df = pd.read_csv(filePath, index_col=False)
            allTeamDataByYearDFArr.append(df)

        df = pd.concat(allTeamDataByYearDFArr)  # create one df for the whole year
        allTeamDataForYearArr = df.to_numpy()

        ### assign team data to map
        for entry in allTeamDataForYearArr:
            teamID = entry[13]
            currentLoggedPlayerIds = teamDataMap[str(year)].keys()
            if str(teamID) in currentLoggedPlayerIds:  # team id already exists, append entry
                teamDataMap[str(year)][str(teamID)].append(entry)
            else:  # team id does not exist for year, add it
                teamDataMap[str(year)][str(teamID)] = [entry]

    return teamDataMap
