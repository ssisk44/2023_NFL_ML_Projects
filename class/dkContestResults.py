import os
import random

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
        self.calculateAverageEarnings()

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
        results = []

        for score in sLOS:
            for singlePayoutStructureList in cPRA:
                results.append([print(payoutLevel[2]) for payoutLevel in singlePayoutStructureList if payoutLevel[1] >= score])
                print(score, results)
                exit()





dkcd = dkContestResults()






