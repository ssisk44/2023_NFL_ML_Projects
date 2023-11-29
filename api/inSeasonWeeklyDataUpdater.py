import os
import time
import dotenv
from api.apiRequests import mySportsFeeds

dotenv.load_dotenv()
absProjectPath = os.getenv("ABS_PROJECT_PATH")
apiObject = mySportsFeeds()

""" THIS SHOULD BE RUN WEEKLY (Tuesday) AS A GENERAL SYSTEM DATA UPDATE FORMALITY...
    - system may require more frequent injury status updates
"""

# def checkIfFileExists(directory:str, subdirectory:str, filename:str):


############################ update system data from api ###########################################

######################## one off data
### players
players_API_URL = apiObject.get_API_URL("players")
api_response = apiObject.send_request(players_API_URL)
apiObject.parse_request_response(api_response, str(absProjectPath) + "data/nfl/players.csv", "csv")

### player injuries
player_injuries_API_URL = apiObject.get_API_URL("player_injuries")
api_response = apiObject.send_request(player_injuries_API_URL)
apiObject.parse_request_response(api_response, str(absProjectPath) + "data/nfl/player_injuries.csv", "csv")

### injury history
injury_history_API_URL = apiObject.get_API_URL("injury_history")
ih_api_response = apiObject.send_request(injury_history_API_URL)
apiObject.parse_request_response(ih_api_response, str(absProjectPath) + "data/nfl/injury_history.csv", "JSON")

thisSeasonYear = os.getenv("CURRENT_SEASON_YEAR")
thisSeasonWeek = os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK")

""" all seasonally incremented data fetched here"""
### seasonal_games
seasonal_games_API_URL = apiObject.get_API_URL("seasonal_games", thisSeasonYear)
api_response = apiObject.send_request(seasonal_games_API_URL)
apiObject.parse_request_response(api_response, str(absProjectPath) + "data/nfl/seasonal_games_schedule/" + str(
    thisSeasonYear) + ".csv", "csv")

### weekly_player_game_logs
weekly_players_API_URL = apiObject.get_API_URL("weekly_player_game_logs", thisSeasonYear, week=thisSeasonWeek)
api_response = apiObject.send_request(weekly_players_API_URL)
apiObject.parse_request_response(api_response, str(absProjectPath) + "data/nfl/weekly_player_game_logs/" + str(
    thisSeasonYear) + "/" + str(thisSeasonWeek) + ".csv", "csv")
time.sleep(3)

### weekly_team_game_logs
weekly_teams_API_URL = apiObject.get_API_URL("weekly_team_game_logs", thisSeasonYear, week=thisSeasonWeek)
api_response = apiObject.send_request(weekly_teams_API_URL)
apiObject.parse_request_response(api_response, str(absProjectPath) + "data/nfl/weekly_team_game_logs/" + str(
    thisSeasonYear) + "/" + str(thisSeasonWeek) + ".csv", "csv")
time.sleep(3)
