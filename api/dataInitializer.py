import os
import time
import dotenv

from api.apiRequests import mySportsFeeds

dotenv.load_dotenv()
absProjectPath = os.getenv("ABS_PROJECT_PATH")
apiObject = mySportsFeeds()


def getWeeksPerSeason(seasonYearNum):
    """helper func for determining season week length"""
    if seasonYearNum < 2021:
        return 17
    return 18


############################ initialize system data from api ###########################################

for thisSeasonYear in range(2017, int(os.getenv('CURRENT_SEASON_YEAR')) + 1):
    """ all seasonally incremented data fetched here"""
    ### seasonal_games
    seasonal_games_API_URL = apiObject.get_API_URL("seasonal_games", thisSeasonYear)
    api_response = apiObject.send_request(seasonal_games_API_URL)
    apiObject.parse_request_response(api_response, str(absProjectPath) + "data/nfl/seasonal_games_schedule/" + str(
        thisSeasonYear) + ".csv", "csv")

    ### seasonal_venues
    seasonal_venues_API_URL = apiObject.get_API_URL("seasonal_venues", thisSeasonYear)
    api_response = apiObject.send_request(seasonal_venues_API_URL)
    apiObject.parse_request_response(api_response,
                                     str(absProjectPath) + "data/nfl/seasonal_venues/" + str(thisSeasonYear) + ".csv",
                                     "csv")

    thisSeasonWeeks = getWeeksPerSeason(thisSeasonYear)
    for thisWeekNum in range(1, thisSeasonWeeks + 1):
        ### weekly_player_game_logs
        weekly_players_API_URL = apiObject.get_API_URL("weekly_player_game_logs", thisSeasonYear, week=thisWeekNum)
        api_response = apiObject.send_request(weekly_players_API_URL)
        apiObject.parse_request_response(api_response, str(absProjectPath) + "data/nfl/weekly_player_game_logs/" + str(
            thisSeasonYear) + "/" + str(thisWeekNum) + ".csv", "csv")
        time.sleep(3)

        ### weekly_team_game_logs
        weekly_teams_API_URL = apiObject.get_API_URL("weekly_team_game_logs", thisSeasonYear, week=thisWeekNum)
        api_response = apiObject.send_request(weekly_teams_API_URL)
        apiObject.parse_request_response(api_response, str(absProjectPath) + "data/nfl/weekly_team_game_logs/" + str(
            thisSeasonYear) + "/" + str(thisWeekNum) + ".csv", "csv")
        time.sleep(3)
