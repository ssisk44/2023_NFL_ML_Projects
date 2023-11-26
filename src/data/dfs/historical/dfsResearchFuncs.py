import gc
import itertools
import os
import sys
from src.constants import getTeamFranchiseIntByCurrentTeamName
import dotenv
import pandas as pd
import datetime
from src.combinatorics import calculateNumberOfCombinations

def main():
    # for now just a simple routine for historical optimal lineup research
    consolidatedDFSData = consolidateAndFilterHistoricalDFSData()
    allPositionsNestedList = getDFSDataBySeasonWeek(consolidatedDFSData, 2023, 11)
    filteredAllPositionsNestedList = filterNestedAllPositionsList(allPositionsNestedList)
    calculateTotalLineupsForNestedPositionArray(filteredAllPositionsNestedList)
    bigShablamo(filteredAllPositionsNestedList, 220, 2023, 11)

def consolidateAndFilterHistoricalDFSData():
    dotenv.load_dotenv()

    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
    historicalDFSPath = absProjectFilepath + "data/dfs/historical/"

    allHistoricalDFSEntries = []
    currentGameIdentifier = ""
    gameIDCounter = 0
    for file in os.listdir(historicalDFSPath):
        df = pd.read_excel(historicalDFSPath + file, header=None)
        np = df.to_numpy()
        for entry in np:
            if str(entry[2]) in ["nan", "DATE"]:
                continue

            thisSeason = entry[0]
            if "Regular Season" not in thisSeason:
                continue

            thisSeasonYear = thisSeason[4:8]
            thisWeek = entry[3]

            # filter game times using date and start time to sunday main slate
            days = ["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"]
            date = str(entry[2])
            thisDate = date[:10]
            dayName = days[datetime.datetime(int(thisDate[0:4]), int(thisDate[5:7]), int(thisDate[8:10])).weekday()]

            thisTime = entry[4]
            timeFirstDigit = int(thisTime[0])
            if dayName != "Sunday":
                continue
            if timeFirstDigit > 6:
                continue

            if currentGameIdentifier not in [str(entry[7]) + str(entry[8]), str(entry[8]) + str(entry[7])]:
                currentGameIdentifier = str(entry[7]) + str(entry[8])
                gameIDCounter += 1

            season = thisSeasonYear
            week = thisWeek
            gameID = gameIDCounter
            player = entry[6]
            team = getTeamFranchiseIntByCurrentTeamName(entry[7])
            otherTeam = getTeamFranchiseIntByCurrentTeamName(entry[8])
            DKPosition = entry[10]
            DKSalary = entry[12]
            DKPoints = entry[14]

            # remove kickers
            if str(DKSalary) == "nan":
                continue

            # prevent division by 0
            DKValue = 0
            if DKPoints != 0:
                DKValue = round(((int(DKPoints) / int(DKSalary)) * 1000), 2)

            allHistoricalDFSEntries.append([season, week, gameID, player, team, otherTeam, DKPosition, DKSalary, DKPoints, DKValue])

    columns = ["season", "week", "gameID", "player", "team", "oppTeam", "DK pos", "DK $", "DK pts", "DK val"]
    pd.DataFrame(allHistoricalDFSEntries, columns=columns).to_csv(absProjectFilepath + "data/dfs/research/allHistoricalData.csv")
    return allHistoricalDFSEntries


def getDFSDataBySeasonWeek(consolidatedDFSData, reqSeason, reqWeek):
    df = pd.DataFrame(consolidatedDFSData, columns=["season", "week", "gameID", "player", "team", "oppTeam", "DK pos", "DK $", "DK pts", "DKValue"])

    QBs = df.loc[(df['season'] == str(reqSeason)) & (df['week'] == reqWeek) & (df['DK pos'] == "QB")]
    RBs = df.loc[(df['season'] == str(reqSeason)) & (df['week'] == reqWeek) & (df['DK pos'] == "RB")]
    WRs = df.loc[(df['season'] == str(reqSeason)) & (df['week'] == reqWeek) & (df['DK pos'] == "WR")]
    TEs = df.loc[(df['season'] == str(reqSeason)) & (df['week'] == reqWeek) & (df['DK pos'] == "TE")]
    FLXs = pd.concat([RBs, WRs, TEs])
    DSTs = df.loc[(df['season'] == str(reqSeason)) & (df['week'] == reqWeek) & (df['DK pos'] == "DST")]


    QBs = QBs.sort_values(by=['DK pts'], ascending=False)
    RBs = RBs.sort_values(by=['DK pts'], ascending=False)
    WRs = WRs.sort_values(by=['DK pts'], ascending=False)
    TEs = TEs.sort_values(by=['DK pts'], ascending=False)
    FLXs = FLXs.sort_values(by=['DK pts'], ascending=False)
    DSTs = DSTs.sort_values(by=['DK pts'], ascending=False)


    # this function should end here but im going to continue to fiddle
    return [QBs, RBs, WRs, TEs, FLXs, DSTs]


def filterNestedAllPositionsList(allPositionsNestedList):
    """
    Due to the combinatorics required to complete all lineups, RBs and WRs salary cutoffs when sorted by descending
    fantasy points scored must allowed leniency top incorporate 1-2 more players (depending on RB or WR) that could
    be a part of the highest scoring team.

    :param allPositionsNestedList:
    :return:
    """
    # cleanse the unrighteous
    filteredAllPositionsNestedList = []

    nestedListPositionCounter = 0 # RB is 1 and WR is 2
    for nestedPositionArr in allPositionsNestedList:
        currentSalaryCutoff = 20000
        filteredPlayers = []
        playerComboAllowanceCounter = 0 # cant cut out some players bleh

        for player in nestedPositionArr.to_numpy():
            playerSalary = player[7]

            if nestedListPositionCounter in [0, 3, 4, 5]:
                if playerSalary >= currentSalaryCutoff:
                    continue
                else:
                    currentSalaryCutoff = playerSalary
                    filteredPlayers.append(player)

            # RB
            elif nestedListPositionCounter == 1:
                if playerSalary >= currentSalaryCutoff and playerComboAllowanceCounter > 1:
                    continue

                elif playerSalary >= currentSalaryCutoff and playerComboAllowanceCounter <= 1:
                    playerComboAllowanceCounter += 1
                    filteredPlayers.append(player)
                    continue

                else:
                    playerComboAllowanceCounter = 0
                    currentSalaryCutoff = playerSalary
                    filteredPlayers.append(player)

            # WR
            elif nestedListPositionCounter == 2:
                if playerSalary >= currentSalaryCutoff and playerComboAllowanceCounter > 2:
                    continue

                elif playerSalary >= currentSalaryCutoff and playerComboAllowanceCounter <= 2:
                    playerComboAllowanceCounter += 1
                    filteredPlayers.append(player)
                    continue

                else:
                    playerComboAllowanceCounter = 0
                    currentSalaryCutoff = playerSalary
                    filteredPlayers.append(player)

        filteredAllPositionsNestedList.append(list(filteredPlayers))
        nestedListPositionCounter += 1

    return filteredAllPositionsNestedList


def calculateTotalLineupsForNestedPositionArray(nestedPositionArrays: list):
    print("QBs:", len(nestedPositionArrays[0]))
    print("RBs:", len(nestedPositionArrays[1]))
    print("WRs:", len(nestedPositionArrays[2]))
    print("TEs:", len(nestedPositionArrays[3]))
    print("FLXs:", len(nestedPositionArrays[4]))
    print("DSTs:", len(nestedPositionArrays[5]))

    ### total number of combinations in retrospect... greater than 1x10^15
    qbc = calculateNumberOfCombinations(len(nestedPositionArrays[0]), 1)
    rbc = calculateNumberOfCombinations(len(nestedPositionArrays[1]), 2)
    wrc = calculateNumberOfCombinations(len(nestedPositionArrays[2]), 3)
    tec = calculateNumberOfCombinations(len(nestedPositionArrays[3]), 1)
    flxc = calculateNumberOfCombinations(len(nestedPositionArrays[4]), 1)
    dstc = calculateNumberOfCombinations(len(nestedPositionArrays[5]), 1)
    print("Maximum number of lineup combinations (NON-PERFECTED): ", qbc * rbc * wrc * tec * flxc * dstc)


def calculateLineupPointsScored(lineup):
    totalPoints = 0
    for player in lineup:
        totalPoints += player[8]
    return totalPoints


def bigShablamo(filteredAllPositionsNestedList, pointsScoredFloor, year, week):
    qbArr = filteredAllPositionsNestedList[0]
    rbArr = filteredAllPositionsNestedList[1]
    wrArr = filteredAllPositionsNestedList[2]
    teArr = filteredAllPositionsNestedList[3]
    flxArr = filteredAllPositionsNestedList[4]
    dArr = filteredAllPositionsNestedList[5]

    rbCombos = list(itertools.combinations(rbArr, 2))
    wrCombos = list(itertools.combinations(wrArr, 3))

    start = datetime.datetime.now()

    # clear memory
    gc.collect()

    allLineups = []
    salaryRemovalCounter = 0
    nameOverlapCounter = 0

    # create an array with string integers that describe their players
    for qb in qbArr:
        qbSalary = int(qb[7])
        qbName = qb[2]

        for rbCombo in rbCombos:
            rbSalary1 = int(rbCombo[0][7])
            rbSalary2 = int(rbCombo[1][7])
            rb1Name = rbCombo[0][3]
            rb2Name = rbCombo[1][3]

            for wrCombo in wrCombos:
                wrSalary1 = int(wrCombo[0][7])
                wrSalary2 = int(wrCombo[1][7])
                wrSalary3 = int(wrCombo[2][7])
                wr1Name = wrCombo[0][3]
                wr2Name = wrCombo[1][3]
                wr3Name = wrCombo[2][3]

                for te in teArr:
                    teSalary = int(te[7])
                    teName = te[3]

                    for flx in flxArr:
                        flxSalary = int(flx[7])
                        flxName = flx[3]

                        if flxName in [qbName, rb1Name, rb2Name, wr1Name, wr2Name, wr3Name, teName]:
                            nameOverlapCounter += 1
                            continue

                        for dst in dArr:
                            dstSalary = int(dst[7])
                            totalSalary = qbSalary + rbSalary1 + rbSalary2 + wrSalary1 + wrSalary2 + wrSalary3 + teSalary + flxSalary + dstSalary
                            if totalSalary > 50000:
                                salaryRemovalCounter += 1
                                continue
                            entry = [qb, rbCombo[0], rbCombo[1], wrCombo[0], wrCombo[1], wrCombo[2], te, flx, dst]
                            allLineups.append(entry)


    end = datetime.datetime.now()
    print("Time taken during combinations processing:", end - start)
    print("All lineups combinations memory in gigabytes:", str(sys.getsizeof(allLineups) / 1000000000) + "GB")
    print("Length of lineup combinations: ", len(allLineups))
    print("Lineups removed due to player name overlap: ", nameOverlapCounter)
    print("Lineups removed due to salary restrictions: ", salaryRemovalCounter)

    counter = 0
    bestLineup = None
    highestScoringLineupTotal = 0
    for entry in allLineups:
        lineupPointsScored = calculateLineupPointsScored(entry)
        if lineupPointsScored >= 220:
            players = []
            for player in entry:
                players.append(player[3])

            if lineupPointsScored > highestScoringLineupTotal:
                bestLineup = players
                highestScoringLineupTotal = lineupPointsScored
            # print(round(lineupPointsScored, 2), players)
            counter += 1

    print("\n", bestLineup, highestScoringLineupTotal)
    print("Number of ghetto remade lineups over 220 points 2023 week 7:", counter)
    print("Percent of ghetto remade lineups over 220 points 2023 week 7:", str(round(counter/len(allLineups) * 100, 6)) + "%")




main()