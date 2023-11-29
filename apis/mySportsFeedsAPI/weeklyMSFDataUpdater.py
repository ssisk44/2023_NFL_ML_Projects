import os
import time
import dotenv
import pandas as pd

from apis.mySportsFeedsAPI.requestMSF import mySportsFeeds

class weeklyMSFDataUpdater:
    """ THIS SHOULD BE RUN WEEKLY (Tuesday) AS A GENERAL SYSTEM DATA UPDATE FORMALITY...
        - system may require more frequent injury status updates
    """
    def __init__(self):
        dotenv.load_dotenv()
        self.absProjectPath = os.getenv("ABS_PROJECT_PATH")
        self.apiObject = mySportsFeeds()
        self.thisSeasonYear = int(os.getenv("CURRENT_SEASON_YEAR"))
        self.lastSeasonWeekCompleted = int(os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK"))

    def updatePlayers(self):
        ### players
        players_API_URL = self.apiObject.get_API_URL("players")
        api_response = self.apiObject.send_request(players_API_URL)
        fullFilepath = str(self.absProjectPath) + "data/nfl/players.csv"
        self.apiObject.parse_request_response(api_response, fullFilepath, "csv")
        self.cleanDataHeaders(fullFilepath)

    def updatePlayerInjuries(self):
        ### player injuries
        player_injuries_API_URL = self.apiObject.get_API_URL("player_injuries")
        api_response = self.apiObject.send_request(player_injuries_API_URL)
        fullFilepath = str(self.absProjectPath) + "data/nfl/player_injuries.csv"
        self.apiObject.parse_request_response(api_response, fullFilepath, "csv")
        self.cleanDataHeaders(fullFilepath)

    def updateInjuryHistory(self):
        ### injury history
        injury_history_API_URL = self.apiObject.get_API_URL("injury_history")
        ih_api_response = self.apiObject.send_request(injury_history_API_URL)
        fullFilepath = str(self.absProjectPath) + "data/nfl/injury_history.csv"
        self.apiObject.parse_request_response(ih_api_response, fullFilepath, "JSON")
        # is JSON... do not clean csv data headers

    def updateSeasonalGames(self):
        ### seasonal_games
        seasonal_games_API_URL = self.apiObject.get_API_URL("seasonal_games", self.thisSeasonYear)
        api_response = self.apiObject.send_request(seasonal_games_API_URL)
        fullFilepath = str(self.absProjectPath) + "data/nfl/seasonal_games_schedule/" + str(
            self.thisSeasonYear) + ".csv"
        self.apiObject.parse_request_response(api_response, fullFilepath, "csv")
        self.cleanDataHeaders(fullFilepath)

    def updateWeeklyPlayerData(self):
        ### weekly_player_game_logs
        weekly_players_API_URL = self.apiObject.get_API_URL("weekly_player_game_logs", self.thisSeasonYear, week=self.lastSeasonWeekCompleted)
        api_response = self.apiObject.send_request(weekly_players_API_URL)
        fullFilepath = str(self.absProjectPath) + "data/nfl/weekly_player_game_logs/" + str(
            self.thisSeasonYear) + "/" + str(self.lastSeasonWeekCompleted) + ".csv"
        self.apiObject.parse_request_response(api_response, fullFilepath, "csv")
        time.sleep(3)
        self.cleanDataHeaders(fullFilepath)

    def updateWeeklyTeamData(self):
        ### weekly_team_game_logs
        weekly_teams_API_URL = self.apiObject.get_API_URL("weekly_team_game_logs", self.thisSeasonYear, week=self.lastSeasonWeekCompleted)
        api_response = self.apiObject.send_request(weekly_teams_API_URL)
        fullFilepath = str(self.absProjectPath) + "data/nfl/weekly_team_game_logs/" + str(
            self.thisSeasonYear) + "/" + str(self.lastSeasonWeekCompleted) + ".csv"
        self.apiObject.parse_request_response(api_response, fullFilepath, "csv")
        time.sleep(3)
        self.cleanDataHeaders(fullFilepath)

    def cleanDataHeaders(self, filepath):
        df = pd.read_csv(filepath)
        df = df.iloc[:, 1:]
        pd.DataFrame(df).to_csv(filepath, index=False)
