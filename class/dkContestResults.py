import os
import random
import matplotlib.pyplot as plt
import dotenv
import numpy as np
import pandas as pd

def replace_all(text, dic):
    dicKeys = list(dic.keys())
    dicValues = list(dic.values())
    for i in range(0, len(dic.keys())):
        text = text.replace(dicKeys[i], dicValues[i])
    return text






class dkContestResults:
    def __init__(self):
        dotenv.load_dotenv()
        absProjectPath = os.getenv("ABS_PROJECT_PATH")
        self.allUnfilteredContestPayoutArr = pd.read_csv(absProjectPath + '/data/dfs/payouts.csv', index_col=None).to_numpy()
        self.allContestsPayoutsList = self.filterAllContestsPayoutsList()
        self.avgEarnings = self.calculateAverageEarnings()
        # self.customPlot(avgEarnings) #pyqt bug

    def filterAllContestsPayoutsList(self):
        allContestsPayoutsList = []
        for cE in self.allUnfilteredContestPayoutArr: # contestEntry = cE
            # cD = cE[1] # contest date
            # cEP = cE[2] # contest entry price
            # cTE = cE[3] # contest total entries
            # cTP = cE[4] # contest total payout
            cPRA = [replace_all(eR, {"]": "", "[": ""}).split(" ") for eR in cE[5:] if type(eR) != float] # contest payout results arr
            allContestsPayoutsList.append(cPRA)
        return allContestsPayoutsList

    def calculateAverageEarnings(self):
        cPRA = self.allContestsPayoutsList # contest payout structure list
        sLOS = np.arange(75, 300.5, 0.5)  # seeded lineup output scores

        scoreResults = []
        for score in sLOS:
            totalPrizePercent = 0

            for singlePayoutStructureList in cPRA:
                prizePercent = self.getSingleContestPrize(score, singlePayoutStructureList)
                totalPrizePercent += prizePercent

            cRT = totalPrizePercent/(100 * len(cPRA)) # avging all payout structure output and converting from percent to decimal
            scoreResults.append([score, round(cRT, 2)])

        return scoreResults

    def getSingleContestPrize(self, score, singlePayoutStructureList):
        previousPrizePercentage = 0
        for payoutLevelIndex in range(0, len(singlePayoutStructureList)):  # find correct score threshold and add percentage prize
            if float(score) > float(singlePayoutStructureList[payoutLevelIndex][1]):
                previousPrizePercentage = float(singlePayoutStructureList[payoutLevelIndex][2])
                if payoutLevelIndex == len(singlePayoutStructureList)-1:
                    return previousPrizePercentage
            else:
                return previousPrizePercentage

    def getScoreAvgPrize(self, score, entryPrice):
        previousMultiplier = 0
        for prizeArrIndex in range(0, len(self.avgEarnings)):
            entry = self.avgEarnings[prizeArrIndex]
            entryScore = entry[0]
            if score > float(entryScore):
                previousMultiplier = entry[1]
                if prizeArrIndex == len(self.avgEarnings)-1:
                    return round(previousMultiplier*entryPrice, 2)
            else:
                return round(previousMultiplier*entryPrice, 2)



dkcd = dkContestResults()

for points in np.arange(75, 300.5, .5):
    prize = dkcd.getScoreAvgPrize(points, 5)
    print("Your lineup scored " + str(points) + " and brought in $" + str(prize))






