import datetime
import sys
import numpy as np
import pandas as pd
import os
import dotenv
import random
import math
import itertools
import gc

"""
    add input for minimum salary required for lineup
    add input for required teams for players in lineup, names and int minimum
    add input for required games for players in lineup, names and int minimum
"""

wantedQBNames = np.array([
    "Sam Howell", "Jordan Love", "Brock Purdy", "Kylar Murray"
])

wantedRBNames = np.array([
    "Austin Ekeler", "Raheem Mostert", "Jerome Ford",
    "Zack Moss", "Brian Robinson Jr.", "Saquon Barkley", "Bijan Robinson", "Jahmyr Gibbs",
    "Kenneth Walker III", "AJ Dillon"
])

wantedWRNames = np.array([
    "Stefon Diggs", "Gabe Davis", "Kendrick Bourne", "Keenan Allen", "Rashee Rice", "Davante Adams",
    "Jakobi Meyers", "Amari Cooper", "Michael Pittman Jr.", "Terry McLaurin", "Curtis Samuel", "Drake London",
    "Amon-Ra St. Brown", "Josh Reynolds", "Kalif Raymond",
    "Zay Flowers", "George Pickens", "Cooper Kupp", "Puka Nacua",
    "Tutu Atwell", "Marquise Brown", "Michael Wilson", "Tyler Lockett",
    "Christian Watson", "Romeo Doubs", "Jayden Reed"
])

wantedTENames = np.array([
    "Travis Kelce", "Logan Thomas", "Kyle Pitts", "Jonnu Smith", "Luke Musgrave"
])

wantedDNames = np.array([
    "Cleveland Browns", "Buffalo Bills"
])

def main():
    dotenv.load_dotenv()

    ###CONTESTS###
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
    contestDataFilepath = absProjectFilepath + "data/dfs/contests/2023-11-19DK.csv"
    combinationsArrContainer = createLineupCombinations(contestDataFilepath)
    parseIntegerOutputCombosToLineups(combinationsArrContainer)

    ###HISTORICAL###
    # convertHistoricalDFSData()
    # createLineupCombinations()



# def createHistoricalLineupCombinations():
#     from src.dfsFunctions.historicalDFSDataFilter import getFinalHistoricalDFSDataArr
#     data = getFinalHistoricalDFSDataArr()
#     print(data[0])


def createLineupCombinations(contestDataFilepath):
    """
    get contest data
    create lineups
        - wanted player filters
            - preselected players
        - contest rule filters
            - at least 3 different teams
            - at least 2 different games
            - less than 5 players from the same team
            - combined salary less than $60,000
            - salary minimum threshold
            - positional requirements
        -
    """
    contestDataArray = pd.read_csv(contestDataFilepath).to_numpy()
    # sortedContestDataArray = sorted(contestDataArray, key=lambda x: x[5], reverse=True)

    # remove players with injury status as "IR"
    filteredContestData1 = filterInjuredPlayers(contestDataArray)
    filteredContestData2 = filterUnwantedPlayers(filteredContestData1)
    print("Total number of players considered:", len(filteredContestData2))


    # calculate total number of lineup combinations from filtered players
    totalCombinationsNumber = calculateTotalNumberOfCombinations(filteredContestData2)
    print("Total lineup combinations: ", totalCombinationsNumber)

    ### attempt to create al combinations
    qbArr = getPlayersByPosition(filteredContestData2, "QB")
    rbArr = getPlayersByPosition(filteredContestData2, "RB")
    wrArr = getPlayersByPosition(filteredContestData2, "WR")
    teArr = getPlayersByPosition(filteredContestData2, "TE")
    flxArr = getPlayersByPosition(filteredContestData2, "FLX")
    dArr = getPlayersByPosition(filteredContestData2, "D")

    rbCombos = list(itertools.combinations(rbArr, 2))
    wrCombos = list(itertools.combinations(wrArr, 3))

    print("Number of QB combinations:", len(qbArr))
    print("Number of RB combinations:", len(rbCombos))
    print("Number of WR combinations:", len(wrCombos))
    print("Number of TE combinations:", len(teArr))
    print("Number of FLX combinations:", len(flxArr))
    print("Number of D combinations:", len(dArr))

    start = datetime.datetime.now()

    # clear memory
    gc.collect()

    allLineupIntegers = []
    salaryRemovalCounter = 0

    #create an array with string integers that describe their players
    for qbIndex in range(0, len(qbArr)):
        playerDataEntryQB = qbArr[qbIndex]
        qbSalary = int(playerDataEntryQB[7])

        for rbIndex in range(0, len(rbCombos)):
            playerDataEntryRB1 = rbCombos[rbIndex][0]
            playerDataEntryRB2 = rbCombos[rbIndex][1]
            rbSalary1 = int(playerDataEntryRB1[7])
            rbSalary2 = int(playerDataEntryRB2[7])

            for wrIndex in range(0, len(wrCombos)):
                playerDataEntryWR1 = wrCombos[wrIndex][0]
                playerDataEntryWR2 = wrCombos[wrIndex][1]
                playerDataEntryWR3 = wrCombos[wrIndex][2]
                wrSalary1 = int(playerDataEntryWR1[7])
                wrSalary2 = int(playerDataEntryWR2[7])
                wrSalary3 = int(playerDataEntryWR3[7])

                for teIndex in range(0, len(teArr)):
                    playerDataEntryTE = teArr[teIndex]
                    teSalary = int(playerDataEntryTE[7])

                    for flxIndex in range(0, len(flxArr)):
                        playerDataEntryFLX = flxArr[flxIndex]
                        flxSalary = int(playerDataEntryFLX[7])

                        for dIndex in range(0, len(dArr)):
                            playerDataEntryD = flxArr[flxIndex]
                            dSalary = int(playerDataEntryD[7])
                            if 57500 <= qbSalary + rbSalary1 + rbSalary2 + wrSalary1 + wrSalary2 + wrSalary3 + teSalary + flxSalary + dSalary > 60000:
                                salaryRemovalCounter += 1
                                continue
                            if random.random() < .00001: #1/100
                                entry = str(qbIndex) + "-" + str(rbIndex) + "-" + str(wrIndex) + "-" + str(
                                    teIndex) + "-" + str(flxIndex) + "-" + str(dIndex)
                                allLineupIntegers.append(entry)




    end = datetime.datetime.now()
    print("Time taken during processing:", end - start)
    print("All lineups combinations memory in gigabytes:", str(sys.getsizeof(allLineupIntegers)/1000000000) + "GB")
    print("Length of integer string combinations map: ", len(allLineupIntegers))
    print("Lineups removed due to salary restrictions: ", salaryRemovalCounter)
    pd.DataFrame(allLineupIntegers, index=None, columns=None).to_csv("C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/tmp/combinatoricsResults.csv")
    return [qbArr, rbCombos, wrCombos, teArr, flxArr, dArr]

def parseIntegerOutputCombosToLineups(combinationsArrContainer):
    qbArr = combinationsArrContainer[0]
    rbCombos = combinationsArrContainer[1]
    wrCombos = combinationsArrContainer[2]
    teArr = combinationsArrContainer[3]
    flxArr = combinationsArrContainer[4]
    dArr = combinationsArrContainer[5]

    combinationOutputs = pd.read_csv("C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/tmp/combinatoricsResults.csv").to_numpy()

    allReconvertedLineups = []
    for comboEntry in combinationOutputs:
        comboStr = comboEntry[1]
        comboStrArr = comboStr.split("-")
        qb = qbArr[int(comboStrArr[0])]
        rb1 = rbCombos[int(comboStrArr[1])][0]
        rb2 = rbCombos[int(comboStrArr[1])][1]
        wr1 = wrCombos[int(comboStrArr[2])][0]
        wr2 = wrCombos[int(comboStrArr[2])][1]
        wr3 = wrCombos[int(comboStrArr[2])][2]
        te = teArr[int(comboStrArr[3])]
        flx = flxArr[int(comboStrArr[4])]
        d = dArr[int(comboStrArr[5])]
        allReconvertedLineups.append([qb, rb1, rb2, wr1, wr2, wr3, te, flx, d])

    pd.DataFrame(allReconvertedLineups).to_csv("C:/Users/samue/PycharmProjects/2023_NFL_ML_Projects/tmp/convertedCombinatoricsResults.csv")

def getPlayersByPosition(contestDataArr, positionName:str):
    filteredPlayerArray = []
    for player in contestDataArr:
        playerPosition = player[2]
        if playerPosition == positionName:
            filteredPlayerArray.append(player)
        elif positionName == "FLX" and playerPosition in ["RB", "WR"]:
            filteredPlayerArray.append(player)
    return filteredPlayerArray

def getPlayerSalary(playerName, playersArr):
    for i in range(0, len(playersArr)):
        if playersArr[i][5] == playerName:
            return int(playersArr[i][7])

def getPlayerFPPG(playerName, playersArr):
    for i in range(0, len(playersArr)):
        if playersArr[i][-1] == playerName:
            return float(playersArr[i][5])

def getPlayerTeamAbbrev(playerName, playersArr):
    for i in range(0, len(playersArr)):
        if playersArr[i][-2] == playerName:
            return playersArr[i][9]

def getPlayerID(playerName, playersArr):
    for i in range(0, len(playersArr)):
        if playersArr[i][3] == playerName:
            return playersArr[i][0]

def checkTeamsForPlayers(playersTeams, playersArr):
    if len(playersTeams) == playersTeams.count(playersTeams[0]):
        return False
    return True

def getPlayerPosition(playerName, playersArr):
    for i in range(0, len(playersArr)):
        if playersArr[0][3] == playerName:
            return playersArr[i][1]

def calculateNumberOfCombinations(n, r):
    numerator = math.factorial(n)
    denominatorMultiplier = math.factorial(r)
    denominatorMultiplicant = math.factorial(n-r)
    denominator = denominatorMultiplier * denominatorMultiplicant
    combinationsNumber = int(numerator/denominator)
    return combinationsNumber

def calculateTotalNumberOfCombinations(contestDataArray):
    QBArr = getPlayersByPosition(contestDataArray, "QB")
    RBArr = getPlayersByPosition(contestDataArray, "RB")
    WRArr = getPlayersByPosition(contestDataArray, "WR")
    TEArr = getPlayersByPosition(contestDataArray, "TE")
    FLXArr = getPlayersByPosition(contestDataArray, "FLX")
    DArr = getPlayersByPosition(contestDataArray, "D")

    qbCombos = calculateNumberOfCombinations(len(QBArr), 1)
    rbCombos = calculateNumberOfCombinations(len(RBArr), 2)
    wrCombos = calculateNumberOfCombinations(len(WRArr), 3)
    teCombos = calculateNumberOfCombinations(len(TEArr), 1)
    flxCombos = calculateNumberOfCombinations(len(FLXArr), 1)
    dCombos = calculateNumberOfCombinations(len(DArr), 1)

    numberOfCombinations = qbCombos * rbCombos * wrCombos * teCombos * flxCombos * dCombos
    return numberOfCombinations

def filterInjuredPlayers(contestDataArray):
    filteredContestDataArray = []
    for player in contestDataArray:
        playerInjuryStatus = player[11]
        if playerInjuryStatus != "IR":
            filteredContestDataArray.append(player)
    return filteredContestDataArray

def filterUnwantedPlayers(contestDataArray, namesByPositionArray=None):
    allWantedNamesArray = np.concatenate((wantedQBNames, wantedRBNames, wantedWRNames, wantedTENames, wantedDNames))
    filteredContestDataArray = []
    names = []
    for player in contestDataArray:
        playerFullName = player[3]
        if playerFullName in allWantedNamesArray:
            names.append(playerFullName)
            filteredContestDataArray.append(player)

    if len(allWantedNamesArray) != len(filteredContestDataArray):
        print('ERROR - while filtering wanted names in contest the resulting array was not equal to the desired amount'
              'of player data to return')
        def determineUnfoundPlayers():
            # ensure all wanted players were added
            for filteredPlayer in filteredContestDataArray:
                playerName = filteredPlayer[3]
                found = False
                for playerNameWanted in allWantedNamesArray:
                    if playerNameWanted == playerName:
                        found = True
                        continue
                if not found:
                    print("Missing a player named: " + str(playerName))
        determineUnfoundPlayers()
    return filteredContestDataArray


