import requests
from config.settings import API_KEY, BASE_URL
from .football_data_service import FootballDataService

class TeamService(FootballDataService):
    def get_data(self, league_id):
        response = requests.get(f"{BASE_URL}/?action=get_teams&league_id={league_id}&APIkey={API_KEY}")
        teams_data = []
        venues_data = []
        players_data = []

        for team in response.json():
            teams_data.append({
                "team_key": team["team_key"],
                "team_name": team["team_name"],
                "team_country": team["team_country"],
                "team_founded": team.get("team_founded"),
                "team_badge": team.get("team_badge")
            })

            venue = team.get("venue", {})
            venues_data.append({
                "team_key": team["team_key"],
                "venue_name": venue.get("venue_name"),
                "venue_address": venue.get("venue_address"),
                "venue_city": venue.get("venue_city"),
                "venue_capacity": venue.get("venue_capacity"),
                "venue_surface": venue.get("venue_surface")
            })

            for player in team.get("players", []):
                players_data.append({
                    "player_id": player["player_id"],
                    "team_key": team["team_key"],
                    "player_name": player["player_name"],
                    "player_complete_name": player.get("player_complete_name"),
                    "player_number": player.get("player_number"),
                    "player_country": player.get("player_country"),
                    "player_type": player.get("player_type"),
                    "player_age": player.get("player_age"),
                    "player_match_played": player.get("player_match_played"),
                    "player_goals": player.get("player_goals"),
                    "player_yellow_cards": player.get("player_yellow_cards"),
                    "player_red_cards": player.get("player_red_cards"),
                    "player_injured": player.get("player_injured") == "Yes",
                    "player_substitute_out": player.get("player_substitute_out"),
                    "player_substitutes_on_bench": player.get("player_substitutes_on_bench"),
                    "player_assists": player.get("player_assists"),
                    "player_birthdate": player.get("player_birthdate"),
                    "player_is_captain": player.get("player_is_captain") == "Yes",
                    "player_rating": player.get("player_rating")
                })

        return teams_data, venues_data, players_data
