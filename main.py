from api.country_service import CountryService
from api.competition_service import CompetitionService
from api.team_service import TeamService
from db.postgresql_service import PostgreSQLService
from api.match_service import MatchService

def main():
    db_service = PostgreSQLService()
    country_service = CountryService()
    competition_service = CompetitionService()
    team_service = TeamService()
    match_service = MatchService()
    
    countries_query = "INSERT INTO Countries (country_id, country_name, country_logo) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
    competitions_query = "INSERT INTO Competitions (league_id, country_id, league_name, league_season, league_logo) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
    teams_query = "INSERT INTO Teams (team_key, team_name, team_country, team_founded, team_badge) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
    venues_query = "INSERT INTO Venues (team_key, venue_name, venue_address, venue_city, venue_capacity, venue_surface) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
    players_query = """
        INSERT INTO Players (
            player_id, team_key, player_name, player_complete_name, player_number, player_country,
            player_type, player_age, player_match_played, player_goals, player_yellow_cards,
            player_red_cards, player_injured, player_substitute_out, player_substitutes_on_bench,
            player_assists, player_birthdate, player_is_captain, player_rating
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (player_id) DO NOTHING
    """
    match_query = """
        INSERT INTO Matches (
            match_id, country_id, country_name, league_id, league_name, match_date, match_status, 
            match_time, match_hometeam_id, match_hometeam_name, match_hometeam_score, 
            match_awayteam_id, match_awayteam_name, match_awayteam_score, 
            match_hometeam_halftime_score, match_awayteam_halftime_score, 
            match_hometeam_extra_score, match_awayteam_extra_score, 
            match_hometeam_penalty_score, match_awayteam_penalty_score, 
            match_hometeam_ft_score, match_awayteam_ft_score, 
            match_hometeam_system, match_awayteam_system, match_live, 
            match_round, match_stadium, match_referee, 
            team_home_badge, team_away_badge, league_logo, country_logo, 
            league_year, fk_stage_key, stage_name
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s
        ) ON CONFLICT (match_id) DO NOTHING;
    """
    goalscorers_query = """
        INSERT INTO Goalscorers (
            match_id, time, home_scorer, home_scorer_id, home_assist, home_assist_id,
            away_scorer, away_scorer_id, away_assist, away_assist_id, score, info, score_info_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
    """
    cards_query = """
        INSERT INTO Cards (
            match_id, time, home_fault, away_fault, card, home_player_id, away_player_id, score_info_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
    """
    substitutions_query = """
        INSERT INTO Substitutions (
            match_id, time, substitution, substitution_player_id, team
        ) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
    """
    lineups_query = """
        INSERT INTO Lineups (
            match_id, player_name, lineup_number, lineup_position, team
        ) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
    """
    statistics_query = """
        INSERT INTO Statistics (
            match_id, type, home_value, away_value
        ) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
    """
    first_half_statistics_query = """
        INSERT INTO FirstHalfStatistics (
            match_id, type, home_value, away_value
        ) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
    """

    countries_data = [(c["country_id"], c["country_name"], c["country_logo"]) for c in country_service.get_data()]
    db_service.insert_data(countries_query, countries_data)

    competitions_data = [(c["league_id"], c["country_id"], c["league_name"], c["league_season"], c["league_logo"]) for c in competition_service.get_data(44)]
    db_service.insert_data(competitions_query, competitions_data)

    teams_data, venues_data, players_data = team_service.get_data(152)
    db_service.insert_data(teams_query, [(t["team_key"], t["team_name"], t["team_country"], t["team_founded"], t["team_badge"]) for t in teams_data])
    db_service.insert_data(venues_query, [(v["team_key"], v["venue_name"], v["venue_address"], v["venue_city"], v["venue_capacity"], v["venue_surface"]) for v in venues_data])
    db_service.insert_data(players_query, [(p["player_id"], p["team_key"], p["player_name"], p["player_complete_name"], p["player_number"], p["player_country"], p["player_type"], p["player_age"], p["player_match_played"], p["player_goals"], p["player_yellow_cards"], p["player_red_cards"], p["player_injured"], p["player_substitute_out"], p["player_substitutes_on_bench"], p["player_assists"], p["player_birthdate"], p["player_is_captain"], p["player_rating"]) for p in players_data])

    matches_data, goalscorers_data, cards_data, substitutions_data, lineups_data, statistics_data, first_half_statistics_data = match_service.get_data("2021-06-22", "2022-11-06", 152)

    match_data = [
        (
            match["match_id"], match["country_id"], match["country_name"], match["league_id"], match["league_name"],
            match["match_date"], match["match_status"], match["match_time"], match["match_hometeam_id"],
            match["match_hometeam_name"], match["match_hometeam_score"], match["match_awayteam_id"],
            match["match_awayteam_name"], match["match_awayteam_score"], match["match_hometeam_halftime_score"],
            match["match_awayteam_halftime_score"], match["match_hometeam_extra_score"], match["match_awayteam_extra_score"],
            match["match_hometeam_penalty_score"], match["match_awayteam_penalty_score"], match["match_hometeam_ft_score"],
            match["match_awayteam_ft_score"], match["match_hometeam_system"], match["match_awayteam_system"],
            match["match_live"] == "1", match["match_round"], match["match_stadium"], match["match_referee"],
            match["team_home_badge"], match["team_away_badge"], match["league_logo"], match["country_logo"],
            match["league_year"], match["fk_stage_key"], match["stage_name"]
        )
        for match in matches_data
    ]
    db_service.insert_data(match_query, match_data)

    db_service.insert_data(goalscorers_query, [(g["match_id"], g["time"], g["home_scorer"], g["home_scorer_id"], g["home_assist"], g["home_assist_id"], g["away_scorer"], g["away_scorer_id"], g["away_assist"], g["away_assist_id"], g["score"], g["info"], g["score_info_time"]) for g in goalscorers_data])
    db_service.insert_data(cards_query, [(c["match_id"], c["time"], c["home_fault"], c["away_fault"], c["card"], c["home_player_id"], c["away_player_id"], c["score_info_time"]) for c in cards_data])
    db_service.insert_data(substitutions_query, [(s["match_id"], s["time"], s["substitution"], s["substitution_player_id"], s["team"]) for s in substitutions_data])
    db_service.insert_data(lineups_query, [(l["match_id"], l["player_name"], l["lineup_number"], l["lineup_position"], l["team"]) for l in lineups_data])
    db_service.insert_data(statistics_query, [(s["match_id"], s["type"], s["home_value"], s["away_value"]) for s in statistics_data])
    db_service.insert_data(first_half_statistics_query, [(s["match_id"], s["type"], s["home_value"], s["away_value"]) for s in first_half_statistics_data])

    db_service.close()

if __name__ == "__main__":
    main()
