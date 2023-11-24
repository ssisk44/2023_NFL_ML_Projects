### mySportsFeedAPI
import base64
import csv
import simplejson as json

import dotenv
import pandas as pd
import requests
import os


class mySportsFeeds:
    """
    ### Core
    # seasonal games DONE
    # daily games XXX - seasonal games can be filtered
    # weekly games XXX - seasonal games can be filtered
    # current season XXX - seasonal games can be filtered
    # latest updates XXX - seasonal games can be filtered
    # seasonal venues DONE

    ### Stats addon
    # daily player game logs XXX - weekly player game logs can be filtered
    # weekly player game logs DONE
    # daily team game logs XXX - weekly player game logs can be filtered
    # weekly team game logs DONE
    # seasonal team stats XXX - can be compiled from team week records
    # seasonal player stats XXX - can be compiled from player week records
    # seasonal standings - NO CSV ******************** NEED A STANDINGS DETERMINATION ALGORITHM ********************

    ### Detailed addon
    # game boxscore XXX - can be formed from weekly player values
    # game play-by-play - maybe be useful later for game scripting research
    # game lineup - starters?
    # player injuries
    # players
    # injury history
    """

    def __init__(self):
        dotenv.load_dotenv()

    def get_API_URL(self, query_type, season_year=None, week=None, gameStr=None):
        if query_type == "seasonal_games":
            return 'https://api.mysportsfeeds.com/v2.1/pull/nfl/' + str(season_year) + '-' + str(
                season_year + 1) + '-regular/games.csv'

        elif query_type == "seasonal_venues":
            return 'https://api.mysportsfeeds.com/v2.1/pull/nfl/' + str(season_year) + '-' + str(
                season_year + 1) + '-regular/venues.csv'

        elif query_type == "weekly_player_game_logs":
            return 'https://api.mysportsfeeds.com/v2.1/pull/nfl/' + str(season_year) + '-' + str(
                season_year + 1) + '-regular/week/'+str(week)+'/player_gamelogs.csv'

        elif query_type == "weekly_team_game_logs":
            return 'https://api.mysportsfeeds.com/v2.1/pull/nfl/' + str(season_year) + '-' + str(
                season_year + 1) + '-regular/week/'+str(week)+'/team_gamelogs.csv'

        elif query_type == "players":
            return 'https://api.mysportsfeeds.com/v2.1/pull/nfl/players.csv'

        # elif query_type == "game_playbyplay":
        #     return 'https://api.mysportsfeeds.com/v2.1/pull/nfl/players.csv'

        # elif query_type == "game_lineup":
        #     return 'https://api.mysportsfeeds.com/v2.1/pull/nfl/' + str(season_year) + '-' + str(
        #         season_year + 1) + '-regular/games/'+gameStr+'lineup.json'

        elif query_type == "injury_history":
            return 'https://api.mysportsfeeds.com/v2.1/pull/nfl/injury_history.json'

        elif query_type == "player_injuries":
            return 'https://api.mysportsfeeds.com/v2.1/pull/nfl/injuries.csv'


        else:
            exit("NO API URL MATCH FOUND IN API REQUESTS")

    def send_request(self, url: str):
        # Request
        try:
            response = requests.get(
                url=url,
                params={
                    "fordate": "20161121"
                },
                headers={
                    "Authorization": "Basic " + base64.b64encode(
                        '{}:{}'.format(os.getenv('MY_SPORTS_FEED_API_KEY'), 'MYSPORTSFEEDS').encode('utf-8')).decode(
                        'ascii')
                }
            )
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))

            return response

        except requests.exceptions.RequestException:
            print('mySportsFeeds send_request method failure: HTTP Request failed')

    def parse_request_response(self, api_response, resultsSaveName:str, parseLanguageType:str):
        if parseLanguageType == "csv":
            store_output = api_response.content.decode('utf-8')
            store_output = csv.reader(store_output.splitlines(), delimiter=',')
            store_output = list(store_output)
            df = pd.DataFrame(store_output)
            df.to_csv(resultsSaveName, header=False, index=False)
            return df

        elif parseLanguageType == "JSON":
            store_output = api_response.json()['playerInjuries']
            with open(resultsSaveName, "w") as outfile:
                if parseLanguageType == "JSON":  # This is JSON
                    json.dump(store_output, outfile)

        # elif parseLanguageType == "XML":
        #     print(api_response.text)








# ### game lineup TODO: Do i need this?
# game_lineup_API_URL = apiObject.get_API_URL("game_lineup", 2022, week=11, gameStr="20230910-ARI-WAS")
# api_response = apiObject.send_request(game_lineup_API_URL)
# apiObject.parse_request_response(api_response, str(absProjectPath) + "tmp/API_Game_Lineup_2022_11.csv","JSON")





