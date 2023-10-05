import os
from dotenv import load_dotenv

load_dotenv()


"""
- a FRANCHISE is a team that maintains the same players, coaches, and staff year to year (regardless of team name)
- a TEAM NAME is a the name which a franchise takes for a period of time, these are occasionally subject to change
"""

"""
FRANCHISES THAT HAVE CHANGED THEIR NAME BY YEAR
Oakland Raiders 1995 to 2019
Las Vegas Raiders 2020 ->

San Diego Chargers 1961 to 2016
Los Angeles Chargers 2017 ->

St. Louis Rams 1995 to 2015
Los Angeles Rams 2016 ->


Washington Redskins ---- to 2019
Washington Football Team 2020 to 2021
Washington Commanders 2023 ->
"""
currentTeamNameToHistoricalTeamNameBySeasonListMap = {
    'Arizona Cardinals': [],
    'Atlanta Falcons': [],
    'Baltimore Ravens': [],
    'Buffalo Bills': [],
    'Carolina Panthers': [],
    'Chicago Bears': [],
    'Cincinnati Bengals': [],
    'Cleveland Browns': [],
    'Dallas Cowboys': [],
    'Denver Broncos': [],
    'Detroit Lions': [],
    'Green Bay Packers': [],
    'Houston Texans': [],
    'Indianapolis Colts': [],
    'Jacksonville Jaguars': [],
    'Kansas City Chiefs': [],
    'Las Vegas Raiders': [],
    'Los Angeles Chargers': [2017, 9999],
    'Los Angeles Rams': [2016, 9999],
    'Miami Dolphins': [],
    'Minnesota Vikings': [],
    'New England Patriots': [],
    'New Orleans Saints': [],
    'New York Giants': [],
    'New York Jets': [],
    'Philadelphia Eagles': [],
    'Pittsburgh Steelers': [],
    'San Diego Chargers': [1961, 2016],
    'San Francisco 49ers': [],
    'Seattle Seahawks': [],
    'St. Louis Rams': [1995, 2015],
    'Tampa Bay Buccaneers': [],
    'Tennessee Titans': [],
    'Washington Commanders': [2023, 9999],
    'Washington Football Team': [2020, 2021],
    'Washington Redskins': [0000, 2019]
}

teamNameToTeamAbbreviationMap = {
    "Arizona Cardinals": "ARZ",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LVR",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Oakland Radiers": "OAK",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Diego Chargers": "SD",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "St. Louis Rams": "STL",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS",
    "Washington Football Team": "WAS",
    "Washington Redskins": "WAS"
}

teamNameToCurrentFranchiseTeamNameMap = {
    "Oakland Raiders": "Las Vegas Raiders",
    "San Diego Chargers": "Los Angeles Chargers",
    "St. Louis Rams": "Los Angeles Rams",
    "Washington Football Team": "Washington Commanders",
    "Washington Redskins": "Washington Commanders"
}

teamNameToSportsReferenceAbbreviation = {
    "Arizona Cardinals": "ARZ",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "rai",
    "Los Angeles Chargers": "sdg",
    "Los Angeles Rams": "ram",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Oakland Raiders": "rai",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Diego Chargers": "sdg",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "St. Louis Rams": "ram",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS",
    "Washington Football Team": "WAS",
    "Washington Redskins": "WAS"
}

def getAllTeamNamesBySeason(season: int):
    """This function returns every team name for a given season"""

    currentSeason = os.environ.get("CURRENT_SEASON_YEAR")
    if season > int(currentSeason):
        return

    teamNames = currentTeamNameToHistoricalTeamNameBySeasonListMap.keys()
    teamsForSeasonList = []
    for teamName in teamNames:
        teamNameEntry = currentTeamNameToHistoricalTeamNameBySeasonListMap[teamName]
        if len(teamNameEntry) == 0:
            teamsForSeasonList.append(teamName)
        else:
            yearStart = teamNameEntry[0]
            yearEnd = teamNameEntry[1]
            if yearStart <= season <= yearEnd:
                teamsForSeasonList.append(teamName)

    return teamsForSeasonList

def getAllTeamNamesForEverySeason():
    seasonMap = {}
    currentSeason = int(os.environ.get("CURRENT_SEASON_YEAR"))
    for year in range(2002, currentSeason+1):
        getAllTeamNamesBySeason(year)


def getCurrentTeamNameForFranchise(teamName: str):
    legacyTeamNames = teamNameToCurrentFranchiseTeamNameMap.keys()

    if teamName not in legacyTeamNames:
        return teamName
    else:
        franchise_current_team_name = teamNameToCurrentFranchiseTeamNameMap[teamName]
        return franchise_current_team_name


