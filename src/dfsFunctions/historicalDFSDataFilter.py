import datetime

import numpy as np
import pandas as pd
import os
import dotenv
import random
import math
import itertools
from src.teamNaming import teamNameFranchiseNumMap

def generateAllHistoricalDFSData():
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
    dataPath = "data/dfs/historical/"
    fullHistoricalDataPath = absProjectFilepath + dataPath

    allHistoricalDataArr = []
    columns = ["Season", "GameID", "Date", "Week", "StartTime", "PlayerID", "Player Name", "TeamName", "OpponentTeamName", "Venue", "DKPosition", "FDPosition", "DKSalary", "FDSalary", "DKPoints", "FDPoints"]
    for filename in os.listdir(fullHistoricalDataPath):
        thisFile = fullHistoricalDataPath + filename
        df = pd.read_excel(thisFile, header=None)
        arr = df.to_numpy()
        for playerData in arr:
            allHistoricalDataArr.append(playerData)
    pd.DataFrame(allHistoricalDataArr, columns=columns, index=None).to_csv(absProjectFilepath + "tmp/xd.csv")

def generateFinalHistoricalDFSData(salaryMin):
    """
    MAKE SURE DATA DOES NOT STILL CONTAIN HEADERS... SEARCH FOR "INFORMATION" TO CHECK
    :return:
    """
    dotenv.load_dotenv()
    data = getAllHistoricalDFSDataDF()
    season = data['Season'].to_numpy()
    week = data['Week'].to_numpy()
    date = data['Date'].to_numpy()
    gameTime = data['StartTime'].to_numpy()
    playerName = data['Player Name'].to_numpy()
    playerID = data['PlayerID'].to_numpy()
    teamName = data['TeamName'].to_numpy()
    opponentName = data['OpponentTeamName'].to_numpy()
    dkPosition = data['DKPosition'].to_numpy()
    fdPosition = data['FDPosition'].to_numpy()
    dkSalary = data['DKSalary'].to_numpy()
    fdSalary = data['FDSalary'].to_numpy()
    dkPoints = data['DKPoints'].to_numpy()
    fdPoints = data['FDPoints'].to_numpy()

    finalHistoricalData = []
    dayRemovalCounter = 0
    emptyPositionCounter = 0
    regularSeasonRemovalCounter = 0
    salaryMinCounter = 0
    for dataIndex in range(0, len(season)):
        #filter playoff weeks
        thisSeason = season[dataIndex]
        if "Regular Season" not in thisSeason:
            regularSeasonRemovalCounter += 1
            continue

        thisSeasonYear = season[dataIndex][4:8]
        thisWeek = week[dataIndex]

        # filter game times using date and start time to sunday main slate
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        thisDate = date[dataIndex][:10]
        dayName = days[datetime.datetime(int(thisDate[0:4]), int(thisDate[5:7]), int(thisDate[8:10])).weekday()]

        thisTime = gameTime[dataIndex]
        timeFirstDigit = int(thisTime[0])
        if dayName != "Sunday" and 0 <= timeFirstDigit <= 5:
            dayRemovalCounter += 1
            continue

        thisPlayerName = playerName[dataIndex]
        thisTeamNameInt = teamNameFranchiseNumMap[teamName[dataIndex]]
        thisOpponentTeamNameInt = teamNameFranchiseNumMap[opponentName[dataIndex]]
        thisPosition = fdPosition[dataIndex]
        thisSalary = fdSalary[dataIndex]
        thisPoints = fdPoints[dataIndex]

        if not thisSalary > salaryMin:
            salaryMinCounter += 1
            continue

        # remove 0 salary players (mid week additions for injuries? most have 0.0 points)
        if math.isnan(thisSalary):
            emptyPositionCounter += 1
            continue


        finalHistoricalData.append([thisSeasonYear, thisWeek, thisPlayerName, thisTeamNameInt, thisOpponentTeamNameInt,
                                    thisPosition, thisSalary, thisPoints])
    print("Data removed because it isnt during main slate:", dayRemovalCounter)
    print("Data removed because of empty player position:", emptyPositionCounter)
    print("Data removed because it wasnt during the regular season:", regularSeasonRemovalCounter)
    print("Data removed because player salary below input threshold:", salaryMinCounter)
    columns = ["season", "week", "player", "teamInt", "oppTeamInt", "position", "salary", "points"]
    df = pd.DataFrame(finalHistoricalData, columns=columns, index=None)
    df.to_csv("C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/tmp/xdFinal.csv")

def getAllHistoricalDFSDataDF():
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
    dataPath = "tmp/xd.csv"
    df = pd.read_csv(absProjectFilepath + dataPath)
    return df

def getFinalHistoricalDFSDataByWeek():
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
    dataPath = "tmp/xdFinal.csv"
    arr = pd.read_csv(absProjectFilepath + dataPath).to_numpy()

    currentWeek = 1
    currentWeeksEntries = []
    allEntries = []
    for entry in arr:
        week = entry[2]
        if week == currentWeek:
            currentWeeksEntries.append(entry)
        else:
            currentWeek = week
            allEntries.append(currentWeeksEntries)
            currentWeeksEntries = []
    return allEntries

def getPlayersByPosition(contestDataArr, positionName:str):
    filteredPlayerArray = []
    for player in contestDataArr:
        playerPosition = player[6]
        if playerPosition == positionName:
            filteredPlayerArray.append(player)
        elif positionName == "FLX" and playerPosition in ["RB", "WR"]:
            filteredPlayerArray.append(player)
    return filteredPlayerArray

def getRandomNumberWithChance(chance: float):
    if random.random() < chance:
        return True
    return False

def calculateTotalNumberOfCombinations(contestDataArray):
    QBArr = getPlayersByPosition(contestDataArray, "QB")
    print("# of QBs:", len(QBArr))
    RBArr = getPlayersByPosition(contestDataArray, "RB")
    print("# of RBs:", len(RBArr))
    WRArr = getPlayersByPosition(contestDataArray, "WR")
    print("# of WRs:", len(WRArr))
    TEArr = getPlayersByPosition(contestDataArray, "TE")
    print("# of TEs:", len(TEArr))
    FLXArr = getPlayersByPosition(contestDataArray, "FLX")
    print("# of FLXs:", len(FLXArr))
    DArr = getPlayersByPosition(contestDataArray, "DST")
    print("# of Ds:", len(DArr))

    qbCombos = calculateNumberOfCombinations(len(QBArr), 1)
    rbCombos = calculateNumberOfCombinations(len(RBArr), 2)
    wrCombos = calculateNumberOfCombinations(len(WRArr), 3)
    teCombos = calculateNumberOfCombinations(len(TEArr), 1)
    flxCombos = calculateNumberOfCombinations(len(FLXArr), 1)
    dCombos = calculateNumberOfCombinations(len(DArr), 1)

    numberOfCombinations = qbCombos * rbCombos * wrCombos * teCombos *flxCombos * dCombos
    return numberOfCombinations

def calculateNumberOfCombinations(n, r):
    numerator = math.factorial(n)
    denominatorMultiplier = math.factorial(r)
    denominatorMultiplicant = math.factorial(n-r)
    denominator = denominatorMultiplier * denominatorMultiplicant
    combinationsNumber = int(numerator/denominator)
    return combinationsNumber

def createAllLineupCombinations(wED: float, salaryMin):
    """
    :param wED: Wanted entries decimal. There are so often more than trillions of combinations per week, only so many can be randomly examined
    :return:
    """
    # separate data by week
    generateFinalHistoricalDFSData(salaryMin)
    contestDataArray = getFinalHistoricalDFSDataByWeek()
    counter = 0
    for weekContestData in contestDataArray:
        print("Total contest combinations:", calculateTotalNumberOfCombinations(weekContestData))
        # get all players by positions
        qbArr = getPlayersByPosition(weekContestData, "QB")
        rbArr = getPlayersByPosition(weekContestData, "RB")
        wrArr = getPlayersByPosition(weekContestData, "WR")
        teArr = getPlayersByPosition(weekContestData, "TE")
        flxArr = getPlayersByPosition(weekContestData, "FLX")
        dArr = getPlayersByPosition(weekContestData, "DST")

        rbCombos = list(itertools.combinations(rbArr, 2))
        wrCombos = list(itertools.combinations(wrArr, 3))

        for qbIndex in range(0, len(qbArr)):
            # playerDataEntryQB = qbArr[qbIndex]
            # playerTeam = playerDataEntryQB[4]
            # qbSalary = int(playerDataEntryQB[7])
            #
            # mapIndex = str(qbIndex)
            # lineupPlayers = [playerDataEntryQB]
            # totalLineupSalary = qbSalary

            for rbIndex in range(0, len(rbCombos)):
                # playerDataEntryRB = rbCombos[rbIndex]

                for wrCombo in range(0, len(wrCombos)):
                    playerDataEntryRB = wrCombos[wrCombo]

                    for teIndex in range(0, len(teArr)):
                        # playerDataEntryRB = teArr[teIndex]
                    #
                        for flxIndex in range(0, len(flxArr)):
                    #         # playerDataEntryRB = flxArr[flxIndex]
                    #
                            for dIndex in range(0, len(dArr)):
                                None

                                #
                                # keepBool = getRandomNumberWithChance(wED)
                                # if not keepBool:
                                #     continue

                                # playerDataEntryRB = dArr[dIndex]
        print(counter)
        exit()

print(datetime.datetime.now())
createAllLineupCombinations(.000000000000001, 5000)
print(datetime.datetime.now())


