import copy
import logging
import os
import datetime
import pandas as pd
from src.dataLoaders.scheduleDataLoaders import getRawScheduleData
from src.teamNaming import getTeamFranchiseInt
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
            gameWeek = game[0]
            gameDay = game[1]
            gameDate = game[2]
            gameTimeTime = game[3][:-2]  #
            gameTimeAbbrev = game[3][-2:]  # AM vs. PM
            # remember the largest season week # to convert playoff string to week
            if len(str(gameWeek)) <= 2:
                lastWeekNum = gameWeek

            # convert from numpy array
            game = list(game)
            newGameEntry = copy.deepcopy(game)
            newGameEntry.append(gameDate)

            # add season year
            newGameEntry.append(seasonCounter)

            # is Playoffs ? (must be before changing playoff weeks to numbers)
            newGameEntry = calculateIsPlayoffs(newGameEntry, int(lastWeekNum))

            # is Day Game ?
            isDayGame = calculateIsDayGame(gameTimeTime, gameTimeAbbrev)
            newGameEntry.append(isDayGame)

            # is Prime time ?
            isPrimeTime = calculateIsPrimeTime(gameWeek, gameDay, gameTimeTime, gameTimeAbbrev)
            newGameEntry.append(isPrimeTime)

            newGameEntry = reformatDataToAwayHomeCategories(newGameEntry)
            newAllSeasonsGamesArr.append(newGameEntry)
            # # keep only played games (MUST BE LAST)
            # if removeUnplayedGamesFromSchedule(game):
            #     processedArr.append(game)
        seasonCounter += 1

    statMap = [offensivePointsMap, offensiveYardsMap, offensiveTOMap, defensivePointsMap, defensiveYardsMap,
               defensiveTOMap] = createStatMap(newAllSeasonsGamesArr, 2002, int(os.getenv("CURRENT_SEASON_YEAR")))

    saveFinalDataForML(newAllSeasonsGamesArr, statMap)




# def removeUnplayedGamesFromSchedule(game, overloadDay=10, overloadMonth=10):
#     # TODO: Reformation - move this filtering functionality to depend on model training/prediction args
#     now = datetime.datetime.now()
#     year = now.year
#     month = now.month
#     day = now.day
#
#     ### WILL CAUSE ISSUES IF NOT CHANGED
#     # used to perform analysis during game days
#     if overloadMonth > 0:
#         month = overloadMonth
#
#     # used to perform analysis during game days
#     if overloadDay > 0:
#         day = overloadDay
#
#     nowDT = datetime.datetime(year, month, day)
#
#     # removes games if they have not been played before the current datetime
#
#     gameYear = int(game[3][:4])
#     gameMonth = int(game[3][5:7])
#     gameDay = int(game[3][8:])
#     gameDT = datetime.datetime(gameYear, gameMonth, gameDay)
#     if nowDT > gameDT:
#         return True
#     return False

def calculateIsPlayoffs(game, previousWeekNum):
    if game[0] == "WildCard":
        game[0] = int(previousWeekNum) + 1
        game.append(1)
    elif game[0] == "Division":
        game[0] = int(previousWeekNum) + 2
        game.append(1)
    elif game[0] == "ConfChamp":
        game[0] = int(previousWeekNum) + 3
        game.append(1)
    elif game[0] == "SuperBowl":
        game[0] = int(previousWeekNum) + 4
        game.append(1)
    else:
        game.append(0)
    return game

def calculateIsDayGame(gameTimeTime, gameTimeAbbrev):
    if int(gameTimeTime[:1]) > 6:
        if gameTimeAbbrev == "AM":
            return 1
        if gameTimeAbbrev == "PM":
            return 0
    else:
        return 1

def calculateIsPrimeTime(gameWeek, gameDay, gameTimeTime, gameTimeAbbrev):
    # playoff is prime time
    if len(str(gameWeek)) > 2:
        return 1

    # single or double night games are prime time
    if gameDay in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
        return 1

    # sunday night or morning games are prime time
    if gameDay == "Sun":
        if int(gameTimeTime[:1]) > 6 and gameTimeAbbrev == "PM":
            return 1
        if gameTimeAbbrev == "AM":
            return 1
        else:
            return 0

def reformatDataToAwayHomeCategories(game):
    winnerTeamName = game[4]
    winnerTeamPPG = game[8]
    winnerTeamYPG = game[10]
    winnerTeamTO = game[11]
    loserTeamName = game[6]
    loserTeamPPG = game[9]
    loserTeamYPG = game[12]
    loserTeamTO = game[13]
    if game[5] == "@" or game[5] == "N":
        return [game[-4], game[0], game[1], game[2], game[3], 0, loserTeamName, loserTeamPPG, loserTeamYPG,
                loserTeamTO, winnerTeamName, winnerTeamPPG, winnerTeamYPG, winnerTeamTO, game[-3], game[-2], game[-1],
                game[7]]
    return [game[-4], game[0], game[1], game[2], game[3], 1, winnerTeamName, winnerTeamPPG, winnerTeamYPG, winnerTeamTO,
            loserTeamName, loserTeamPPG, loserTeamYPG, loserTeamTO, game[-3], game[-2], game[-1], game[7]]

def getGamesBySeason(seasonsGamesArr, seasonYear):
    seasonGames = []
    for game in seasonsGamesArr:
        if int(game[0]) == seasonYear:
            seasonGames.append(game)
        if int(game[0]) > seasonYear:
            break
    return seasonGames

def createStatMap(allSeasonsGames, startYear, endYear):
    # STAT AVERAGING
    offensivePoints = {}
    offensiveYards = {}
    offensiveTO = {}
    defensivePoints = {}
    defensiveYards = {}
    defensiveTO = {}

    for year in range(int(startYear), int(endYear)+1):
        # initialize data year for entries
        offensivePoints[year] = {}
        offensiveYards[year] = {}
        offensiveTO[year] = {}
        defensivePoints[year] = {}
        defensiveYards[year] = {}
        defensiveTO[year] = {}

        seasonGames = getGamesBySeason(allSeasonsGames, year)

        for game in seasonGames:
            season = game[0]
            week = game[1]

            homeTeamName = game[6]
            homeTeamPoints = game[7]
            homeTeamYards = game[8]
            homeTeamTO = game[9]
            awayTeamName = game[10]
            awayTeamPoints = game[11]
            awayTeamYards = game[12]
            awayTeamTO = game[13]

            teamNameMap = offensivePoints[season].keys()
            if homeTeamName not in teamNameMap:
                offensivePoints[season][homeTeamName] = [homeTeamPoints]
                offensiveYards[season][homeTeamName] = [homeTeamYards]
                offensiveTO[season][homeTeamName] = [homeTeamTO]
                defensivePoints[season][homeTeamName] = [awayTeamPoints]
                defensiveYards[season][homeTeamName] = [awayTeamYards]
                defensiveTO[season][homeTeamName] = [awayTeamTO]
            else:
                offensivePoints[season][homeTeamName].append(homeTeamPoints)
                offensiveYards[season][homeTeamName].append(homeTeamYards)
                offensiveTO[season][homeTeamName].append(homeTeamTO)
                defensivePoints[season][homeTeamName].append(awayTeamPoints)
                defensiveYards[season][homeTeamName].append(awayTeamYards)
                defensiveTO[season][homeTeamName].append(awayTeamTO)

            if awayTeamName not in teamNameMap:
                offensivePoints[season][awayTeamName] = [awayTeamPoints]
                offensiveYards[season][awayTeamName] = [awayTeamYards]
                offensiveTO[season][awayTeamName] = [awayTeamTO]
                defensivePoints[season][awayTeamName] = [homeTeamPoints]
                defensiveYards[season][awayTeamName] = [homeTeamYards]
                defensiveTO[season][awayTeamName] = [homeTeamTO]

            else:
                offensivePoints[season][awayTeamName].append(awayTeamPoints)
                offensiveYards[season][awayTeamName].append(awayTeamYards)
                offensiveTO[season][awayTeamName].append(awayTeamTO)
                defensivePoints[season][awayTeamName].append(homeTeamPoints)
                defensiveYards[season][awayTeamName].append(homeTeamYards)
                defensiveTO[season][awayTeamName].append(homeTeamTO)

    return [offensivePoints, offensiveYards, offensiveTO, defensivePoints, defensiveYards, defensiveTO]

def returnStatMapValues(year, week, teamName, statMap):
    retValues = []
    currentSeasonYear = int(os.getenv("CURRENT_SEASON_YEAR"))
    currentSeasonWeek = int(os.getenv("CURRENT_SEASON_WEEK"))
    for map in statMap:
        if year == currentSeasonYear and int(week) >= currentSeasonWeek:
            values = map[year][teamName][:int(currentSeasonWeek)-1]
            cleanedList = [x for x in values if str(x) != 'nan']
            cleanedValue = round(mean(cleanedList), 2)
            retValues.append(cleanedValue)
        elif int(week) == 1:
            if year == currentSeasonYear:
                values = map[year][teamName][:int(currentSeasonWeek)]
                cleanedList = [x for x in values if str(x) != 'nan']
                cleanedValue = round(mean(cleanedList), 2)
                retValues.append(cleanedValue)
            else:
                retValues.append(round(mean(map[year][teamName]), 2))
        else:
            retValues.append(round(mean(map[year][teamName][:int(week)]), 2))
    return retValues

def saveFinalDataForML(allSeasonsGames, statmap):
    # TODO: Smolder - Get all/include all game/schedule value
    # finalCols = ["season", "weekNum", "isDayGame", "isPrimetime", "isPlayoffs", "homeIsWinner", "homeFranchiseInt",
    #              "homeOffPointsAvg", "homeOffYardsAvg", "homeOffTOAvg", "homeDefPointsAvg", "homeDefYardsAvg",
    #              "homeDefTOAvg", "awayFranchiseInt", "awayOffPointsAvg", "awayOffYardsAvg", "awayOffTOAvg",
    #              "awayDefPointsAvg", "awayDefYardsAvg", "awayDefTOAvg", "Home Score", "Away Score", "Score Diff"]
    currentSeasonYear = int(os.getenv("CURRENT_SEASON_YEAR"))
    currentSeasonWeek = int(os.getenv("CURRENT_SEASON_WEEK"))

    gameCounter = 0
    mlArr = []
    for game in allSeasonsGames:
        season = game[0]
        gameDate = game[3]
        week = game[1]
        if season == currentSeasonYear and week > currentSeasonWeek:
            break
        homeIsWinner = game[5]
        homeTeamName = game[6]
        homeTeamFranchiseInt = getTeamFranchiseInt(homeTeamName)
        homeTeamPoints = game[7]
        homeTeamStatMapValues = returnStatMapValues(season, week, homeTeamName, statmap)

        awayTeamName = game[10]
        awayTeamFranchiseInt = getTeamFranchiseInt(awayTeamName)
        awayTeamPoints = game[11]

        gameCounter += 1
        awayTeamStatMapValues = returnStatMapValues(season, week, awayTeamName, statmap)
        arr = [
            game[0],
            game[1],
            game[-4],
            game[-3],
            game[-2],
            game[5],
            homeTeamFranchiseInt,
            homeTeamStatMapValues[0],
            homeTeamStatMapValues[1],
            homeTeamStatMapValues[2],
            homeTeamStatMapValues[3],
            homeTeamStatMapValues[4],
            homeTeamStatMapValues[5],
            awayTeamFranchiseInt,
            awayTeamStatMapValues[0],
            awayTeamStatMapValues[1],
            awayTeamStatMapValues[2],
            awayTeamStatMapValues[3],
            awayTeamStatMapValues[4],
            awayTeamStatMapValues[5],
            homeTeamPoints,
            awayTeamPoints,
            homeTeamPoints - awayTeamPoints,
            gameDate,
            homeTeamName,
            awayTeamName,
            homeIsWinner
        ]
        mlArr.append(arr)
    finalCols = [
        "season", "weekNum", "isDayGame", "isPrimetime", "isPlayoffs", "homeIsWinner", "homeFranchiseInt",
        "homeOffPointsAvg", "homeOffYardsAvg", "homeOffTOAvg", "homeDefPointsAvg", "homeDefYardsAvg",
        "homeDefTOAvg", "awayFranchiseInt", "awayOffPointsAvg", "awayOffYardsAvg", "awayOffTOAvg",
        "awayDefPointsAvg", "awayDefYardsAvg", "awayDefTOAvg", "Home Score", "Away Score", "Score Diff",
        'Game Date', 'homeTeamName', 'awayTeamName', 'homeIsWinner'
    ]
    mainDirectory = os.getenv("ABS_PROJECT_PATH")
    pd.DataFrame(mlArr, columns=finalCols).to_csv(mainDirectory + 'data/final/schedule/NFLScheduleAndResultsProcessed.csv', index=False)