import requests
import pandas as pd


class SportsDataPGA:
    """Wrapper for sportsdata.io PGA tour API: https://sportsdata.io/developers/api-documentation/golf#"""

    def __init__(self):
        self.auth = {'Ocp-Apim-Subscription-Key': 'abd80dc64b0e4ba4b274c80fe2ecc495'}
        self.headers = {**self.auth}

    def getPlayers(self):

        """Get request for "Players" endpoint

            :Input - None

            :Returns -
                - players_df (DataFrame) - Contains most recent base player information
        """

        players = requests.get("https://fly.sportsdata.io/golf/v2/json/Players"
                                            , headers=self.headers)
        if players.status_code == 200:
            print('Successfully pulled all base player data from players endpoint!')
        else:
            print(f'There was an issue pulling base player data, status code: {players.status_code}')
        players_df = pd.json_normalize(players.json())

        return players_df

    def getTournaments(self):

        """Get request for "Tournaments" endpoint

            :Input - None

            :Returns -
                - tournaments_df (DataFrame) - Contains most recent tournament scheduling information
        """

        tournaments = requests.get("https://fly.sportsdata.io/golf/v2/json/Tournaments"
                                            , headers=self.headers)
        if tournaments.status_code == 200:
            print('Successfully pulled all tournament scheduling data from Tournaments endpoint!')
        else:
            print(f'There was an issue pulling tournament scheduling data, status code: {tournaments.status_code}')
        tournaments_df = pd.json_normalize(tournaments.json())

        # Rounds is its own JSON object so need to separate it out (Not included in this)
        return tournaments_df.drop('Rounds', axis=1)



