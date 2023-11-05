import copy
import logging
import os
import datetime
import pandas as pd
from src.dataLoaders.scheduleDataLoaders import getRawScheduleData
from src import constants as Constants
from statistics import mean

def transformScheduleData():
    """"""
    allSeasonsGamesArr = getRawScheduleData()

    newAllSeasonsGamesArr = []
    seasonCounter = 2002
    for season in allSeasonsGamesArr:
        logging.info("Transforming Schedule Data for:" + str(season[0][2][:4]))
        lastWeekNum = 1
        for game in season:
            thisGameEntry = []

            gameSeason = seasonCounter
            gameWeek = game[0]
            gameDayAbrrev = game[1]
            gameDate = game[2]
            gameTime = game[3]
            gameLink = game[7]

            # calculate away and home team name indexes
            awayTeamIndex = 6
            awayScoreIndex = 9
            homeTeamIndex = 4
            homeScoreIndex = 8
            homeIsWinner = 1
            if game[5] == '@':
                awayTeamIndex = 4
                awayScoreIndex = 8
                homeTeamIndex = 6
                homeScoreIndex = 9
                homeIsWinner = 0

            awayTeamFranchiseInt = Constants.getTeamFranchiseIntByCurrentTeamName(game[awayTeamIndex])
            homeTeamFranchiseInt = Constants.getTeamFranchiseIntByCurrentTeamName(game[homeTeamIndex])
            awayScore = game[awayScoreIndex]
            homeScore = game[homeScoreIndex]

            awayTeamName = Constants.getTeamNameForYearAndFranchiseName(year=gameSeason, franchiseInt=awayTeamFranchiseInt)
            homeTeamName = Constants.getTeamNameForYearAndFranchiseName(year=gameSeason, franchiseInt=homeTeamFranchiseInt)

            gameID = str(gameSeason) + "-" + str(gameWeek) + "-" + str(awayTeamFranchiseInt) + "-" + str(homeTeamFranchiseInt)

            thisGameEntry.append(gameID)
            thisGameEntry.append(gameSeason)
            thisGameEntry.append(gameWeek)
            thisGameEntry.append(awayTeamFranchiseInt)
            thisGameEntry.append(homeTeamFranchiseInt)
            thisGameEntry.append(gameDayAbrrev)
            thisGameEntry.append(gameDate)
            thisGameEntry.append(gameTime)

            # remember the largest season week # to convert playoff string to week
            if len(str(gameWeek)) <= 2:
                lastWeekNum = gameWeek

            thisGameEntry.append(calculateIsPlayoffs(gameWeek))
            thisGameEntry.append(calculateIsMainSlateGame(gameWeek, gameDayAbrrev, gameTime))
            thisGameEntry.append(awayTeamName)
            thisGameEntry.append(awayScore)
            thisGameEntry.append(homeTeamName)
            thisGameEntry.append(homeScore)
            thisGameEntry.append(homeIsWinner)
            thisGameEntry.append(gameLink)

            # add game entry to final array
            newAllSeasonsGamesArr.append(thisGameEntry)

        seasonCounter += 1

    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    nflScheduleDataFilepath = absProjectPath + "data/schedule/NFL-Historical-Schedule-And-Results.csv"
    pd.DataFrame(newAllSeasonsGamesArr, columns=Constants.nflScheduleGamesColumns).to_csv(nflScheduleDataFilepath, index=False)

def calculateIsPlayoffs(weekNum):
    if len(str(weekNum)) > 2:
        return int(1)
    return int(0)

def calculateIsMainSlateGame(gameWeek, gameDayAbrrev, gameTime):
    # playoff is prime time
    if len(str(gameWeek)) > 2:
        return 0

    # single or double night games are prime time
    if gameDayAbrrev in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
        return 0

    # sunday night or morning games are prime time
    if gameDayAbrrev == "Sun":
        gameTimeArr = gameTime.split(":")
        gameTimeHour = gameTimeArr[0]
        gameTimeMinutes = gameTimeArr[1][:2]
        gameTimeAbbrev = gameTimeArr[1][2:]


        if 1 <= int(gameTimeHour) <= 5 and gameTimeAbbrev == "PM":
            return 1
        else:
            return 0

transformScheduleData()