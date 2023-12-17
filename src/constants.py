import os
import dotenv
import pandas as pd

dotenv.load_dotenv()
currentSeasonYear = int(os.getenv("CURRENT_SEASON_YEAR"))

# mySportsData API Data Constants


# BigBallData Historical DFS Contest Data Constants
bdbColumns = ['Season', 'GameID', 'Date', 'Week', 'Game Time', 'PlayerID', 'Player Name', 'Player Team', 'Player Opponent Team', 'Venue Ownership', 'DK Position', 'FD Position', 'DK Salary', 'FD Salary', 'DK Points', 'FD Points']

# msf constant
# msfPlayerWeeklyColumns = ['#Game ID', '#Game Date', '#Game Time', '#Away Team ID', '#Away Team Abbr.', '#Away Team City', '#Away Team Name', '#Home Team ID', '#Home Team Abbr.', '#Home Team City', '#Home Team Name', '#Venue ID', '#Venue Name', '#Player ID', '#LastName', '#FirstName', '#Jersey Num', '#Position', '#Height', '#Weight', '#Birth Date', '#Age', '#Birth City', '#Birth Country', '#Rookie', '#Team ID', '#Team Abbr.', '#Team City', '#Team Name', '#PassAttempts', '#PassCompletions', '#PassPct', '#PassAttemptsPerGame', '#PassYards', '#PassYardsPerAtt', '#PassYardsPerGame', '#PassTD', '#PassTDPct', '#PassInt', '#PassIntPct', '#PassLng', '#PassAvg', '#Pass20Plus', '#Pass40Plus', '#PassSacks', '#PassSackY', '#QbRating', '#RushAttempts', '#RushAttemptsPerGame', '#RushYards', '#RushAverage', '#RushYardsPerGame', '#RushTD', '#RushLng', '#Rush1stDowns', '#Rush1stDownsPct', '#Rush20Plus', '#Rush40Plus', '#RushFumbles', '#Targets', '#Receptions', '#RecYards', '#RecAverage', '#RecYardsPerGame', '#RecTD', '#RecLng', '#Rec1stDowns', '#Rec20Plus', '#Rec40Plus', '#RecFumbles', '#TackleSolo', '#TackleTotal', '#TackleAst', '#Sacks', '#SackYds', '#TacklesForLoss', '#Interceptions', '#IntTD', '#IntYds', '#IntAverage', '#IntLng', '#PassesDefended', '#Stuffs', '#Safeties', '#StuffYds', '#Kb', '#Fumbles', '#FumLost', '#FumForced', '#FumOwnRec', '#FumOppRec', '#FumRecYds', '#FumTotalRec', '#FumTD', '#KrRet', '#KrYds', '#KrAvg', '#KrLng', '#KrTD', '#Kr20Plus', '#Kr40Plus', '#KrFC', '#KrFum', '#PrRet', '#PrYds', '#PrAvg', '#PrLng', '#PrTD', '#Pr20Plus', '#Pr40Plus', '#PrFC', '#PrFum', '#FgBlk', '#FgMade', '#FgAtt', '#FgPct', '#FgMade1_19', '#FgAtt1_19', '#Fg1_19Pct', '#FgMade20_29', '#FgAtt20_29', '#Fg20_29Pct', '#FgMade30_39', '#FgAtt30_39', '#Fg30_39Pct', '#FgMade40_49', '#FgAtt40_49', '#Fg40_49Pct', '#FgMade50Plus', '#FgAtt50Plus', '#Fg50PlusPct', '#FgLng', '#XpBlk', '#XpMade', '#XpAtt', '#XpPct', '#FgAndXpPts', '#KoPct', '#Kickoffs', '#KoYds', '#KoOOB', '#KoAvg', '#KoTB', '#KoRet', '#KoRetYds', '#KoRetAvgYds', '#KoTD', '#KoOS', '#KoOSR', '#Punts', '#PuntYds', '#PuntNetYds', '#PuntLng', '#PuntAvg', '#PuntNetAvg', '#PuntBlk', '#PuntOOB', '#PuntDown', '#PuntIn20', '#PuntIn20Pct', '#PuntTB', '#PuntTBPct', '#PuntFC', '#PuntRet', '#PuntRetYds', '#PuntRetAvg', '#GamesStarted', '#TwoPtAtt', '#TwoPtMade', '#TwoPtPassAtt', '#TwoPtPassMade', '#TwoPtPassRec', '#TwoPtRushAtt']
# msfPlayerTrainingVariables = ['#Game Date', '#Game Time', '#Position', '#Height', '#Weight', '#Age', '#Rookie', '#PassAttempts', '#PassCompletions', '#PassPct', '#PassAttemptsPerGame', '#PassYards', '#PassYardsPerAtt', '#PassYardsPerGame', '#PassTD', '#PassTDPct', '#PassInt', '#PassIntPct', '#PassLng', '#PassAvg', '#Pass20Plus', '#Pass40Plus', '#PassSacks', '#PassSackY', '#QbRating', '#RushAttempts', '#RushAttemptsPerGame', '#RushYards', '#RushAverage', '#RushYardsPerGame', '#RushTD', '#RushLng', '#Rush1stDowns', '#Rush1stDownsPct', '#Rush20Plus', '#Rush40Plus', '#RushFumbles', '#Targets', '#Receptions', '#RecYards', '#RecAverage', '#RecYardsPerGame', '#RecTD', '#RecLng', '#Rec1stDowns', '#Rec20Plus', '#Rec40Plus', '#GamesStarted', '#TwoPtAtt', '#TwoPtMade', '#TwoPtPassAtt', '#TwoPtPassMade', '#TwoPtPassRec', '#TwoPtRushAtt']

# msf to bdb constants


# data columns
gDNumCols = ['#Game Week', "#Away Team ID", "#Home Team ID", '#Away Score Total', '#Home Score Total']
gDCatCols = ['#Game Date', '#Game Time']

# ttDNumNonAvgCols = ['#Team ID']
ttDNumCols = ['#PassAttempts', '#PassCompletions', '#PassPct', '#PassAttemptsPerGame', '#PassGrossYards', '#PassAvg', '#PassNetYards', '#PassYardsPerAtt', '#PassYardsPerGame',
             '#PassTD', '#PassTDPct', '#PassInt', '#PassIntPct', '#PassLng', '#Pass20Plus', '#Pass40Plus', '#PassSacks', '#PassSackY', '#QBRating', '#RushAttempts', '#RushAttemptsPerGame', '#RushYards', '#RushAverage',
             '#RushYardsPerGame', '#RushTD', '#RushLng', '#Rush1stDowns', '#Rush1stDownsPct', '#Rush20Plus', '#Rush40Plus', '#RushFumbles', '#Receptions', '#RecYards', '#RecAverage', '#RecYardsPerGame', '#RecTD', '#RecLng',
             '#Rec1stDowns', '#Rec20Plus', '#Rec40Plus', '#RecFumbles', '#TackleSolo', '#TackleTotal', '#TackleAst', '#Sacks', '#SackYds', '#TacklesForLoss', '#Interceptions', '#IntTD', '#IntYds', '#IntAverage', '#IntLng',
             '#PassesDefended', '#Stuffs', '#StuffYds', '#KB', '#Safeties', '#Fumbles', '#FumLost', '#FumForced', '#FumOwnRec', '#FumOppRec', '#FumRecYds', '#FumTotalRec', '#FumTD', '#KrRet', '#KrYds', '#KrAvg', '#KrLng',
             '#KrTD', '#Kr20Plus', '#Kr40Plus', '#KrFC', '#KrFum', '#PrRet', '#PrYds', '#PrAvg', '#PrLng', '#PrTD', '#Pr20Plus', '#Pr40Plus', '#PrFC', '#PrFum', '#FgBlk', '#FgMade', '#FgAtt', '#FgPct', '#FgMade1_19',
             '#FgAtt1_19', '#Fg1_19Pct', '#FgMade20_29', '#FgAtt20_29', '#Fg20_29Pct', '#FgMade30_39', '#FgAtt30_39', '#Fg30_39Pct', '#FgMade40_49', '#FgAtt40_49', '#Fg40_49Pct', '#FgMade50Plus', '#FgAtt50Plus',
             '#Fg50PlusPct', '#FgLng', '#XpBlk', '#XpMade', '#XpAtt', '#XpPct', '#FgAndXpPts', '#KoPct', '#Kickoffs', '#KoYds', '#KoOOB', '#KoAvg', '#KoTB', '#KoRet', '#KoRetYds', '#KoRetAvgYds', '#KoTD', '#KoOS', '#KoOSR',
             '#Punts', '#PuntYds', '#PuntNetYds', '#PuntLng', '#PuntAvg', '#PuntNetAvg', '#PuntBlk', '#PuntOOB', '#PuntDown', '#PuntIn20', '#PuntIn20Pct', '#PuntTB', '#PuntTBPct', '#PuntFC', '#PuntRet', '#PuntRetYds',
             '#PuntRetAvg', '#TwoPtAtt', '#TwoPtMade', '#TwoPtPassAtt', '#TwoPtPassMade', '#TwoPtRushAtt', '#TwoPtRushMade', '#FirstDownsTotal', '#FirstDownsPass', '#FirstDownsRush', '#FirstDownsPenalty', '#ThirdDowns',
             '#ThirdDownsAtt', '#ThirdDownsPct', '#FourthDowns', '#FourthDownsAtt', '#FourthDownsPct', '#Penalties', '#PenaltyYds', '#OffensePlays', '#OffenseYds', '#OffenseAvgYds', '#TotalTD', '#Wins', '#Losses', '#Ties',
             '#OTWins', '#OTLosses', '#WinPct', '#PointsFor', '#PointsAgainst', '#PointDifferential', 'DK Salary', 'DK Points', "PlayerDK200ptSalaryEff", "PlayerDKEffLabel"]
tDCatCols = ['Venue Ownership']

ptDNumCols = ['#PassAttempts', '#PassCompletions', '#PassPct', '#PassAttemptsPerGame', '#PassYards', '#PassYardsPerAtt', '#PassYardsPerGame', '#PassTD', '#PassTDPct', '#PassInt',
             '#PassIntPct', '#PassLng', '#PassAvg', '#Pass20Plus','#Pass40Plus', '#PassSacks', '#PassSackY', '#QbRating', '#RushAttempts', '#RushAttemptsPerGame',
             '#RushYards', '#RushAverage', '#RushYardsPerGame', '#RushTD', '#RushLng', '#Rush1stDowns', '#Rush1stDownsPct',
             '#Rush20Plus', '#Rush40Plus', '#RushFumbles', '#Targets', '#Receptions', '#RecYards', '#RecAverage', '#RecYardsPerGame', '#RecTD', '#RecLng', '#Rec1stDowns', '#Rec20Plus', '#Rec40Plus', '#RecFumbles',
             '#TackleSolo', '#TackleTotal', '#TackleAst', '#Sacks', '#SackYds', '#TacklesForLoss', '#Interceptions', '#IntTD', '#IntYds', '#IntAverage', '#IntLng', '#PassesDefended', '#Stuffs', '#Safeties', '#StuffYds', '#Kb',
             '#Fumbles', '#FumLost', '#FumForced', '#FumOwnRec', '#FumOppRec', '#FumRecYds', '#FumTotalRec', '#FumTD', '#KrRet', '#KrYds', '#KrAvg', '#KrLng', '#KrTD', '#Kr20Plus', '#Kr40Plus', '#KrFC', '#KrFum', '#PrRet', '#PrYds',
             '#PrAvg', '#PrLng', '#PrTD', '#Pr20Plus', '#Pr40Plus', '#PrFC', '#PrFum', '#FgBlk', '#FgMade', '#FgAtt', '#FgPct', '#FgMade1_19', '#FgAtt1_19', '#Fg1_19Pct', '#FgMade20_29', '#FgAtt20_29', '#Fg20_29Pct', '#FgMade30_39',
             '#FgAtt30_39', '#Fg30_39Pct', '#FgMade40_49', '#FgAtt40_49', '#Fg40_49Pct', '#FgMade50Plus', '#FgAtt50Plus', '#Fg50PlusPct', '#FgLng', '#XpBlk', '#XpMade', '#XpAtt', '#XpPct', '#FgAndXpPts', '#KoPct', '#Kickoffs',
             '#KoYds', '#KoOOB', '#KoAvg', '#KoTB', '#KoRet', '#KoRetYds', '#KoRetAvgYds', '#KoTD', '#KoOS', '#KoOSR', '#Punts', '#PuntYds', '#PuntNetYds', '#PuntLng', '#PuntAvg', '#PuntNetAvg', '#PuntBlk', '#PuntOOB', '#PuntDown',
             '#PuntIn20', '#PuntIn20Pct', '#PuntTB', '#PuntTBPct', '#PuntFC', '#PuntRet', '#PuntRetYds', '#PuntRetAvg', '#GamesStarted', '#TwoPtAtt', '#TwoPtMade', '#TwoPtPassAtt', '#TwoPtPassMade', '#TwoPtPassRec', '#TwoPtRushAtt',
             '#TwoPtRushMade', '#OffenseSnaps', '#DefenseSnaps', '#SpecialTeamSnaps', 'DK Salary', 'DK Points', "PlayerDK200ptSalaryEff", "PlayerDKEffLabel"]
ptDCatCols = ['DK Position', '#Position', '#Rookie'] #birth country '#Height', '#Weight', '#Age'

vDNumCols = ['Latitude', 'Longitude', 'Azimuth Angle', 'Elevation']
vDCatCols = ['Venue Country', 'Field Type', 'Stadium Type']

trainingOutputCols = ['DK Points', "PlayerDK200ptSalaryEff", "PlayerDKEffLabel"]

def convertColumnsToTemporal(columns, temporalArr):
    convertedColumns = []
    for temporalVal in temporalArr:
        for column in columns:
            column = column + str(temporalVal)
            convertedColumns.append(column)
    return convertedColumns


def convertCatColumnToValues(columnName, columnValue):
    if columnName == "Venue Ownership":
        d = {
            'Home': 1,
            'Road': 0
        }
        return d[str(columnName)][str(columnValue)]

    elif columnName == "#Game Date": # game month
        gameMonth = columnValue[5:7]
        return int(gameMonth)

    elif columnName == "#Game Time": # is primetime?
        time = columnValue[:-2]
        hours = (time[:time.index(':')]-4) % 24
        if 12 <= hours <= 18:
            return 0
        else:
            return 1

    elif columnName == "DK Position":
        d = {
            'QB': 1,
            'RB': 2,
            'WR': 3,
            'TE': 4,
            'DST': 5
        }
        return d[str(columnName)][str(columnValue)]
    elif columnName == "#Position":
        d = {
            'QB': 1,
            'RB': 2,
            'WR': 3,
            'TE': 4,
            'FB': 5
        }
        return d[str(columnName)][str(columnValue)]
    elif columnName == "#Rookie":
        d = {
            'Y': 1,
            'N': 0
        }
        return d[str(columnName)][str(columnValue)]













teamAbbrevToDepthChartLinkMap = {
    # AFC EAST
    'BUF': 'https://www.espn.com/nfl/team/depth/_/name/buf/buffalo-bills',
    'MIA': 'https://www.espn.com/nfl/team/depth/_/name/mia/miami-dolphins',
    'NE': 'https://www.espn.com/nfl/team/depth/_/name/ne/new-england-patriots',
    'NYJ': 'https://www.espn.com/nfl/team/depth/_/name/nyj/new-york-jets',

    # AFC NORTH
    'BAL': 'https://www.espn.com/nfl/team/depth/_/name/bal/baltimore-ravens',
    'CIN': 'https://www.espn.com/nfl/team/depth/_/name/cin/cincinnati-bengals',
    'CLE': 'https://www.espn.com/nfl/team/_/name/cle/cleveland-browns',
    'PIT': 'https://www.espn.com/nfl/team/_/name/pit/pittsburgh-steelers',

    # AFC SOUTH
    'HOU': 'https://www.espn.com/nfl/team/_/name/hou/houston-texans',
    'IND': 'https://www.espn.com/nfl/team/_/name/ind/indianapolis-colts',
    'JAx': 'https://www.espn.com/nfl/team/_/name/jax/jacksonville-jaguars',
    'TEN': 'https://www.espn.com/nfl/team/_/name/ten/tennessee-titans',

    # AFC WEST
    'DEN': 'https://www.espn.com/nfl/team/_/name/den/denver-broncos',
    'KC': 'https://www.espn.com/nfl/team/_/name/kc/kansas-city-chiefs',
    'LV': 'https://www.espn.com/nfl/team/_/name/lv/las-vegas-raiders',
    'LAC': 'https://www.espn.com/nfl/team/_/name/lac/los-angeles-chargers',

    # NFC EAST
    'DAL': 'https://www.espn.com/nfl/team/_/name/dal/dallas-cowboys',
    'NYG': 'https://www.espn.com/nfl/team/_/name/nyg/new-york-giants',
    'PHI': 'https://www.espn.com/nfl/team/_/name/phi/philadelphia-eagles',
    'WAS': 'https://www.espn.com/nfl/team/_/name/wsh/washington-commanders',

    # NFC NORTH
    'CHI': 'https://www.espn.com/nfl/team/_/name/chi/chicago-bears',
    'DET': 'https://www.espn.com/nfl/team/_/name/det/detroit-lions',
    'GB': 'https://www.espn.com/nfl/team/_/name/gb/green-bay-packers',
    'MIN': 'https://www.espn.com/nfl/team/_/name/min/minnesota-vikings',

    # NFC SOUTH
    'ATL': 'https://www.espn.com/nfl/team/_/name/atl/atlanta-falcons',
    'CAR': 'https://www.espn.com/nfl/team/_/name/car/carolina-panthers',
    'NO': 'https://www.espn.com/nfl/team/_/name/no/new-orleans-saints',
    'TB': 'https://www.espn.com/nfl/team/_/name/tb/tampa-bay-buccaneers',

    # NFC WEST
    'ARI': 'https://www.espn.com/nfl/team/_/name/ari/arizona-cardinals',
    'LA': 'https://www.espn.com/nfl/team/_/name/lar/los-angeles-rams',
    'SF': 'https://www.espn.com/nfl/team/_/name/sf/san-francisco-49ers',
    'SEA': 'https://www.espn.com/nfl/team/_/name/sea/seattle-seahawks'
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

