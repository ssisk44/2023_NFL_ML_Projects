import webbrowser
from src import constants

"""
This script is used to prevent me from having to manually open all the the depth chart to perform research
- Get team abbreviations for all main slate games on season & week
- Open team depth chart for each abbreviation
"""


def openTeamDepthChartForTeamAbbrev(teamAbbrev):
    return webbrowser.open_new_tab(constants.teamAbbrevToDepthChartLinkMap[teamAbbrev])







