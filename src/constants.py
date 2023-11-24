import os
import dotenv

dotenv.load_dotenv()
currentSeasonYear = int(os.getenv("CURRENT_SEASON_YEAR"))

rawScheduleDataHeader = ['Week #', 'Day', 'Date', 'Time', 'Winning Team', '@', 'Losing Team', 'Link', 'W Score', 'L Score', 'W Yds', 'W TO', 'L Yds', 'L TO']

nflScheduleGamesColumns = ["gameID", "gameSeason", "gameWeek", "awayTeamFranchiseInt", "homeTeamFranchiseInt",
                                    "gameDayAbbrev", "gameDate", "gameTime", "isPlayoffGame", "isMainSlate",
                                    "awayTeamName", "awayScore", "homeTeamName", "homeScore", "homeIsWinner",
                                    "gameLink"]
gameInfoArrColumns = ["Won Toss", "Stadium Type", "Stadium Surface", "Game Duration", "Attendance", "Weather", "ML", "OU"]
snapCountDataColumns = ['Player', 'Pos', 'OffSnapNum', 'OffPct', 'DefSnapNum', 'DefPct', 'SptSnapNum', 'SptPct', 'playerID']

teamNameToFranchiseAbbrevMap = {
    "Arizona Cardinals": "crd",
    "Atlanta Falcons": "atl",
    "Baltimore Ravens": "rav",
    "Buffalo Bills": "buf",
    "Carolina Panthers": "car",
    "Chicago Bears": "chi",
    "Cincinnati Bengals": "cin",
    "Cleveland Browns": "cle",
    "Dallas Cowboys": "dal",
    "Denver Broncos": "den",
    "Detroit Lions": "det",
    "Green Bay Packers": "gnb",
    "Houston Texans": "htx",
    "Indianapolis Colts": "clt",
    "Jacksonville Jaguars": "jax",
    "Kansas City Chiefs": "kan",
    "Las Vegas Raiders": "rai",
    "Los Angeles Chargers": "sdg",
    "Los Angeles Rams": "ram",
    "Miami Dolphins": "mia",
    "Minnesota Vikings": "min",
    "New England Patriots": "nwe",
    "New Orleans Saints": "nor",
    "New York Giants": "nyg",
    "New York Jets": "nyj",
    "Oakland Raiders": "rai",
    "Philadelphia Eagles": "phi",
    "Pittsburgh Steelers": "pit",
    "San Diego Chargers": "sdg",
    "San Francisco 49ers": "sfo",
    "Seattle Seahawks": "sea",
    "St. Louis Rams": "ram",
    "Tampa Bay Buccaneers": "tam",
    "Tennessee Titans": "oti",
    "Washington Commanders": "was",
    "Washington Football Team": "was",
    "Washington Redskins": "was"
}

franchiseIntYearToTeamNameMap = {
    0: {'Arizona Cardinals': [1994, currentSeasonYear]},
    1: {'Atlanta Falcons': [1966, currentSeasonYear]},
    2: {'Baltimore Ravens': [1996, currentSeasonYear]},
    3: {'Buffalo Bills': [1960, currentSeasonYear]},
    4: {'Carolina Panthers': [1995, currentSeasonYear]},
    5: {'Chicago Bears': [1922, currentSeasonYear]},
    6: {'Cincinnati Bengals': [1968, currentSeasonYear]},
    7: {'Cleveland Browns': [1946, currentSeasonYear]},
    8: {'Dallas Cowboys': [1960, currentSeasonYear]},
    9: {'Denver Broncos': [1960, currentSeasonYear]},
    10: {'Detroit Lions': [1934, currentSeasonYear]},
    11: {'Green Bay Packers': [1921, currentSeasonYear]},
    12: {'Houston Texans': [2002, currentSeasonYear]},
    13: {'Indianapolis Colts': [1984, currentSeasonYear]},
    14: {'Jacksonville Jaguars': [1995, currentSeasonYear]},
    15: {'Kansas City Chiefs': [1963, currentSeasonYear]},
    16: {
        'Las Vegas Raiders': [2020, currentSeasonYear],
        'Oakland Raiders': [1995, 2019]
    },
    17: {
        'Los Angeles Chargers': [2017, currentSeasonYear],
        'San Diego Chargers': [1961, 2016]
    },
    18: {
        'Los Angeles Rams': [2016, currentSeasonYear],
        'St. Louis Rams': [1995, 2015]
    },
    19: {'Miami Dolphins': [1966, currentSeasonYear]},
    20: {'Minnesota Vikings': [1961, currentSeasonYear]},
    21: {'New England Patriots': [1960, currentSeasonYear]},
    22: {'New Orleans Saints': [1967, currentSeasonYear]},
    23: {'New York Giants': [1925, currentSeasonYear]},
    24: {'New York Jets': [1960, currentSeasonYear]},
    25: {'Philadelphia Eagles': [1944, currentSeasonYear]},
    26: {'Pittsburgh Steelers': [1945, currentSeasonYear]},
    27: {'San Fransisco 49ers': [1946, currentSeasonYear]},
    28: {'Seattle Seahawks': [1976, currentSeasonYear]},
    29: {'Tampa Bay Buccaneers': [1976, currentSeasonYear]},
    30: {'Tennessee Titans': [1960, currentSeasonYear]},
    31: {
        'Washington Commanders': [2022, currentSeasonYear],
        'Washington Football Team': [2020, 2021],
        'Washington Redskins': [1937, 2019]
    }
}

teamNameToFranchiseNumMap = {
    "Arizona Cardinals": "0",
    "Atlanta Falcons": "1",
    "Baltimore Ravens": "2",
    "Buffalo Bills": "3",
    "Carolina Panthers": "4",
    "Chicago Bears": "5",
    "Cincinnati Bengals": "6",
    "Cleveland Browns": "7",
    "Dallas Cowboys": "8",
    "Denver Broncos": "9",
    "Detroit Lions": "10",
    "Green Bay Packers": "11",
    "Houston Texans": "12",
    "Indianapolis Colts": "13",
    "Jacksonville Jaguars": "14",
    "Kansas City Chiefs": "15",
    "Las Vegas Raiders": "16",
    "Oakland Raiders": "16",
    "Los Angeles Chargers": "17",
    "San Diego Chargers": "17",
    "Los Angeles Rams": "18",
    "St. Louis Rams": "18",
    "Miami Dolphins": "19",
    "Minnesota Vikings": "20",
    "New England Patriots": "21",
    "New Orleans Saints": "22",
    "New York Giants": "23",
    "New York Jets": "24",
    "Philadelphia Eagles": "25",
    "Pittsburgh Steelers": "26",
    "San Francisco 49ers": "27",
    "Seattle Seahawks": "28",
    "Tampa Bay Buccaneers": "29",
    "Tennessee Titans": "30",
    "Washington Commanders": "31",
    "Washington Football Team": "31",
    "Washington Redskins": "31"
}

def getTeamNameForYearAndFranchiseName(year:int, franchiseInt: int):
    franchiseNamesList = list(franchiseIntYearToTeamNameMap[franchiseInt].values())
    if len(franchiseNamesList) == 1:
        return list(franchiseIntYearToTeamNameMap[franchiseInt].keys())[0]
    else:
        for dateRangeArrIndex in range(0, len(franchiseNamesList)):
            yearStart = franchiseNamesList[dateRangeArrIndex][0]
            yearEnd = franchiseNamesList[dateRangeArrIndex][1]
            if yearStart <= year <= yearEnd:
                return str(list(franchiseIntYearToTeamNameMap[franchiseInt].keys())[dateRangeArrIndex])
# print(getTeamNameForYearAndFranchiseName(2019, 31))

def getTeamFranchiseIntByCurrentTeamName(franchiseName):
    teamFranchiseInt = teamNameToFranchiseNumMap[franchiseName]
    return int(teamFranchiseInt)

def getCurrentTeamNameByFranchiseInt(franchiseInt: int):
    currentTeamName = list(teamNameToFranchiseNumMap.keys())[franchiseInt]
    return currentTeamName

