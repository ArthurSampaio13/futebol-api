import requests
from config.settings import API_KEY, BASE_URL
from .football_data_service import FootballDataService

class MatchService(FootballDataService):
    def get_data(self, start, end, league_id):
        response = requests.get(f"{BASE_URL}/?action=get_events&from={start}&to={end}&league_id={league_id}&APIkey={API_KEY}")
        match_data = response.json()
        
        matches_data = []
        goalscorers_data = []
        cards_data = []
        substitutions_data = []
        lineups_data = []
        statistics_data = []
        first_half_statistics_data = []

        for match in match_data:
            matches_data.append({
                "match_id": match["match_id"],
                "country_id": match["country_id"],
                "country_name": match["country_name"],
                "league_id": match["league_id"],
                "league_name": match["league_name"],
                "match_date": match["match_date"],
                "match_status": match["match_status"],
                "match_time": match["match_time"],
                "match_hometeam_id": match["match_hometeam_id"],
                "match_hometeam_name": match["match_hometeam_name"],
                "match_hometeam_score": match["match_hometeam_score"],
                "match_awayteam_id": match["match_awayteam_id"],
                "match_awayteam_name": match["match_awayteam_name"],
                "match_awayteam_score": match["match_awayteam_score"],
                "match_hometeam_halftime_score": match["match_hometeam_halftime_score"],
                "match_awayteam_halftime_score": match["match_awayteam_halftime_score"],
                "match_hometeam_extra_score": match.get("match_hometeam_extra_score", ""),
                "match_awayteam_extra_score": match.get("match_awayteam_extra_score", ""),
                "match_hometeam_penalty_score": match.get("match_hometeam_penalty_score", ""),
                "match_awayteam_penalty_score": match.get("match_awayteam_penalty_score", ""),
                "match_hometeam_ft_score": match.get("match_hometeam_ft_score", ""),
                "match_awayteam_ft_score": match.get("match_awayteam_ft_score", ""),
                "match_hometeam_system": match.get("match_hometeam_system", ""),
                "match_awayteam_system": match.get("match_awayteam_system", ""),
                "match_live": match["match_live"],
                "match_round": match["match_round"],
                "match_stadium": match["match_stadium"],
                "match_referee": match.get("match_referee", ""),
                "team_home_badge": match.get("team_home_badge", ""),
                "team_away_badge": match.get("team_away_badge", ""),
                "league_logo": match.get("league_logo", ""),
                "country_logo": match.get("country_logo", ""),
                "league_year": match.get("league_year", ""),
                "fk_stage_key": match.get("fk_stage_key", ""),
                "stage_name": match.get("stage_name", "")
            })

            for scorer in match.get("goalscorer", []):
                goalscorers_data.append({
                    "match_id": match["match_id"],
                    "time": scorer["time"],
                    "home_scorer": scorer.get("home_scorer", ""),
                    "home_scorer_id": scorer.get("home_scorer_id", ""),
                    "home_assist": scorer.get("home_assist", ""),
                    "home_assist_id": scorer.get("home_assist_id", ""),
                    "score": scorer.get("score", ""),
                    "away_scorer": scorer.get("away_scorer", ""),
                    "away_scorer_id": scorer.get("away_scorer_id", ""),
                    "away_assist": scorer.get("away_assist", ""),
                    "away_assist_id": scorer.get("away_assist_id", ""),
                    "info": scorer.get("info", ""),
                    "score_info_time": scorer.get("score_info_time", "")
                })

            for card in match.get("cards", []):
                cards_data.append({
                    "match_id": match["match_id"],
                    "time": card.get("time", ""),
                    "home_fault": card.get("home_fault", ""),
                    "away_fault": card.get("away_fault", ""),
                    "card": card.get("card", ""),
                    "home_player_id": card.get("home_player_id", ""),
                    "away_player_id": card.get("away_player_id", ""),
                    "score_info_time": card.get("score_info_time", "")
                })

            for substitution in match.get("substitutions", {}).get("home", []):
                substitutions_data.append({
                    "match_id": match["match_id"],
                    "time": substitution.get("time", ""),
                    "substitution": substitution.get("substitution", ""),
                    "substitution_player_id": substitution.get("substitution_player_id", ""),
                    "team": "home"
                })
            for substitution in match.get("substitutions", {}).get("away", []):
                substitutions_data.append({
                    "match_id": match["match_id"],
                    "time": substitution.get("time", ""),
                    "substitution": substitution.get("substitution", ""),
                    "substitution_player_id": substitution.get("substitution_player_id", ""),
                    "team": "away"
                })

            for lineup in match.get("lineup", {}).get("home", {}).get("starting_lineups", []):
                lineups_data.append({
                    "match_id": match["match_id"],
                    "player_name": lineup.get("lineup_player", ""),
                    "lineup_number": lineup.get("lineup_number", ""),
                    "lineup_position": lineup.get("lineup_position", ""),
                    "team": "home"
                })
            for lineup in match.get("lineup", {}).get("away", {}).get("starting_lineups", []):
                lineups_data.append({
                    "match_id": match["match_id"],
                    "player_name": lineup.get("lineup_player", ""),
                    "lineup_number": lineup.get("lineup_number", ""),
                    "lineup_position": lineup.get("lineup_position", ""),
                    "team": "away"
                })

            for stat in match.get("statistics", []):
                statistics_data.append({
                    "match_id": match["match_id"],
                    "type": stat["type"],
                    "home_value": stat["home"],
                    "away_value": stat["away"]
                })

            for stat in match.get("statistics_1half", []):
                first_half_statistics_data.append({
                    "match_id": match["match_id"],
                    "type": stat["type"],
                    "home_value": stat["home"],
                    "away_value": stat["away"]
                })

        return matches_data, goalscorers_data, cards_data, substitutions_data, lineups_data, statistics_data, first_half_statistics_data
