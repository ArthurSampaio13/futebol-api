import requests
from config.settings import API_KEY, BASE_URL
from .football_data_service import FootballDataService

class CountryService(FootballDataService):
    def get_data(self):
        response = requests.get(f"{BASE_URL}/?action=get_countries&APIkey={API_KEY}")
        return [
            {"country_id": country["country_id"], 
             "country_name": country["country_name"], 
             "country_logo" : country['country_logo']
             } for country in response.json()]