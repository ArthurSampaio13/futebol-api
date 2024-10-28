import requests
from config.settings import API_KEY, BASE_URL
from .football_data_service import FootballDataService

class CompetitionService(FootballDataService):
    def get_data(self, country_id):
        response = requests.get(f"{BASE_URL}/?action=get_leagues&country_id={country_id}&APIkey={API_KEY}")
        return [
            {
                "league_id": competition["league_id"],
                "country_id": competition["country_id"],
                "league_name": competition["league_name"],
                "league_season": competition["league_season"],
                "league_logo" : competition["league_logo"]
            }
            for competition in response.json()
        ]