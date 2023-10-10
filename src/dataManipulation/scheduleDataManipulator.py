import os
import datetime
import pandas as pd
from src.utilityFunctions import getScheduleDataForRange


def processScheduleData():
    """ DATA PROCESSING REQUIREMENTS
    - add season year (DONE)
    - isDayGame
    - isPrimetime True if playoffs, sunday night past 7pm, monday night, thursday night


    - isPlayoffs True if week is non int
    - convert all week nums
        - wildcard = 18
        - division = 19
        - conference champ = 20
        - superbowl = 21
    """
    yearStart = int(os.environ.get("FIRST_SEASON_YEAR"))
    yearEnd = int(os.environ.get("CURRENT_SEASON_YEAR"))
    allSeasonsGameArr = getScheduleDataForRange(yearStart, yearEnd + 1)

    processedArr = []
    seasonCounter = yearStart
    for season in allSeasonsGameArr:
        print("Manipulating Schedule Data for: ", season[0][-4])
        lastWeekNum = "1"
        for game in season:
            gameWeek = game[0]
            gameDay = game[1]
            gameTimeTime = game[3][:-1]  #
            gameTimeAbbrev = game[3][-2:]  # AM vs. PM

            # add season year
            game = addSeasonYearToEntry(game, seasonCounter)

            # record highest season week num to convert playoff string to week
            if len(str(gameWeek)) <= 2:
                lastWeekNum = gameWeek

            # is Playoffs ? (must be before changing playoff weeks to numbers)
            game = calculateIsPlayoffs(game, lastWeekNum)

            # is Day Game ?
            isDayGame = calculateIsDayGame(gameTimeTime, gameTimeAbbrev)
            game.append(isDayGame)

            # is Prime time ?
            isPrimeTime = calculateIsPrimeTime(gameWeek, gameDay, gameTimeTime, gameTimeAbbrev)
            game.append(isPrimeTime)

            game = reformatDataToAwayHomeCategories(game)

            # keep only played games (MUST BE LAST)
            if removeUnplayedGamesFromSchedule(game):
                processedArr.append(game)

        seasonCounter += 1

    # cant find whats adding the last random value:

    ### write processed data to final
    header = ['Season', 'Week', 'Day', 'Date', 'Time', 'Home is Winner', 'Home Team Name', 'Home Points', 'Home Yards', 'Home TO',
              'Away Team Name', 'Away Points', 'Away Yards', 'Away TO', "isDayGame", "isPrimetime", "isPlayoffs", 'Box Score Link']
    pd.DataFrame(processedArr[:-2]).to_csv('data/Processed/Schedules/NFLScheduleAndResultsProcessed.csv', index=False,
                                      header=header)

def addSeasonYearToEntry(game, year):
    g = list(game)  # was a numpy array
    g.append(year)
    return g

def removeUnplayedGamesFromSchedule(game, overloadDay=10, overloadMonth=10):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    ### WILL CAUSE ISSUES IF NOT CHANGED
    # used to perform analysis during game days
    if overloadMonth > 0:
        month = overloadMonth

    # used to perform analysis during game days
    if overloadDay > 0:
        day = overloadDay

    nowDT = datetime.datetime(year, month, day)

    # removes games if they have not been played before the current datetime

    gameYear = int(game[3][:4])
    gameMonth = int(game[3][5:7])
    gameDay = int(game[3][8:])
    gameDT = datetime.datetime(gameYear, gameMonth, gameDay)
    if nowDT > gameDT:
        return True

    return False

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
    return [game[-4], game[0], game[1], game[2], game[3], 1, winnerTeamName, winnerTeamPPG, winnerTeamYPG, winnerTeamTO, loserTeamName, loserTeamPPG, loserTeamYPG, loserTeamTO, game[-3], game[-2], game[-1], game[7]]



