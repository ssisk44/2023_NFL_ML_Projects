import logging
import math

import dotenv
import pandas as pd
import os
from src.functions.data.msf.player.playerDataFuncs import getMSFPlayerFromPlayerDF


def createPlayerIDBridge(bdbDF, msfDF, year, week):
    for i1,bdbPlayerEntry in bdbDF.iterrows():
        # process bdb player data
        bdbPlayerName = bdbPlayerEntry['Player Name']
        # process player name
        bdbPlayerName = bdbPlayerName.lower()
        bdbPlayerName = bdbPlayerName.replace(".", "")
        splitBDBPlayerName = bdbPlayerName.split(" ")
        if splitBDBPlayerName[-1] in ['jr', 'sr', "ii", "iii", "iv", "v"]:
            bdbPlayerName = ' '.join(splitBDBPlayerName[:-1])


        bdbPlayerTeamName = bdbPlayerEntry["Player Team"]
        bdbHomeTeamName = bdbPlayerEntry["Player Opponent Team"]
        isHome = bdbPlayerEntry["Venue Ownership"] == "Home"
        if isHome:
            bdbHomeTeamName = bdbPlayerEntry['Player Team']
        bdbPlayerDKPosition = bdbPlayerEntry['DK Position']
        bdbPlayerDKSalary = bdbPlayerEntry['DK Salary']
        bdbPlayerDKPoints = bdbPlayerEntry['DK Points']

        if math.isnan(bdbPlayerDKSalary): #dk salary nan... no player record found in msf -> SOLUTION: throw away if salary of nan
            continue

        # get corresponding msf player
        msfPlayerEntry = getMSFPlayerFromPlayerDF(msfDF, bdbPlayerName, bdbHomeTeamName)
        if msfPlayerEntry is None:
            if bdbPlayerDKPoints == 0.0: #they did not have a record because they didnt play
                continue
            logging.info([bdbPlayerName, bdbPlayerTeamName, str(year), str(week) ,str(bdbPlayerDKPoints), str(bdbPlayerDKSalary)])



def getPlayerIDfromPlayerIDBridge(gameID, msfPlayerID):
    """ """