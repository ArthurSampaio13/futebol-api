"""create initial tables

Revision ID: 07412c210025
Revises: 
Create Date: 2024-10-25 10:50:31.333810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07412c210025'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE Countries (
        country_id VARCHAR(50) PRIMARY KEY,
        country_name VARCHAR(255) NOT NULL UNIQUE,
        country_logo VARCHAR(255)
);
        
    CREATE TABLE Competitions (
        league_id VARCHAR(50) PRIMARY KEY,
        country_id VARCHAR(50) REFERENCES Countries(country_id),
        league_name VARCHAR(255) NOT NULL,
        league_season VARCHAR(20),
        league_logo VARCHAR(255),
        UNIQUE (league_id, league_season)
);

    CREATE TABLE Teams (
        team_key VARCHAR(50) PRIMARY KEY,
        team_name VARCHAR(255) NOT NULL,
        team_country VARCHAR(255),
        team_founded VARCHAR(20),
        team_badge VARCHAR(255),
        league_id VARCHAR(50) REFERENCES Competitions(league_id),
        UNIQUE (team_key)  
);

    CREATE TABLE Venues (
        venue_id SERIAL PRIMARY KEY,
        team_key VARCHAR(50) REFERENCES Teams(team_key),
        venue_name VARCHAR(255),
        venue_address VARCHAR(255),
        venue_city VARCHAR(255),
        venue_capacity VARCHAR(15),
        venue_surface VARCHAR(50),
        UNIQUE (team_key)  
);

    CREATE TABLE Players (
        player_id VARCHAR(50) PRIMARY KEY,
        team_key VARCHAR(50) REFERENCES Teams(team_key),
        player_name VARCHAR(255),
        player_complete_name VARCHAR(255),
        player_number VARCHAR(100),
        player_country VARCHAR(255),
        player_type VARCHAR(50),
        player_age VARCHAR(100),
        player_match_played VARCHAR(10) DEFAULT '0',
        player_goals VARCHAR(10) DEFAULT '0',
        player_yellow_cards VARCHAR(10) DEFAULT '0',
        player_red_cards VARCHAR(10) DEFAULT '0',
        player_injured VARCHAR(10) DEFAULT 'NO',
        player_substitute_out VARCHAR(10) DEFAULT '0',
        player_substitutes_on_bench VARCHAR(10) DEFAULT '0',
        player_assists VARCHAR(10) DEFAULT '0',
        player_birthdate VARCHAR(10),
        player_is_captain VARCHAR(10) DEFAULT 'FALSE',
        player_rating VARCHAR(10),
        UNIQUE (player_id)  
);
        
    CREATE TABLE Matches (
        match_id VARCHAR(50) PRIMARY KEY,
        country_id VARCHAR(50),
        country_name VARCHAR(100),
        league_id VARCHAR(50),
        league_name VARCHAR(100),
        match_date VARCHAR(50),
        match_status VARCHAR(20),
        match_time VARCHAR(50),
        match_hometeam_id VARCHAR(50),
        match_hometeam_name VARCHAR(100),
        match_hometeam_score VARCHAR(50),
        match_awayteam_id VARCHAR(50),
        match_awayteam_name VARCHAR(100),
        match_awayteam_score VARCHAR(50),
        match_hometeam_halftime_score VARCHAR(50),
        match_awayteam_halftime_score VARCHAR(50),
        match_hometeam_extra_score VARCHAR(50),
        match_awayteam_extra_score VARCHAR(50),
        match_hometeam_penalty_score VARCHAR(50),
        match_awayteam_penalty_score VARCHAR(50),
        match_hometeam_ft_score VARCHAR(50),
        match_awayteam_ft_score VARCHAR(50),
        match_hometeam_system VARCHAR(50),
        match_awayteam_system VARCHAR(50),
        match_live VARCHAR(50),
        match_round VARCHAR(20),
        match_stadium VARCHAR(100),
        match_referee VARCHAR(100),
        team_home_badge VARCHAR(255),
        team_away_badge VARCHAR(255),
        league_logo VARCHAR(255),
        country_logo VARCHAR(255),
        league_year VARCHAR(20),
        fk_stage_key VARCHAR(50),
        stage_name VARCHAR(50)
);
    CREATE TABLE Goalscorers (
        id SERIAL PRIMARY KEY,
        match_id VARCHAR(50) REFERENCES Matches(match_id) ON DELETE CASCADE,
        time VARCHAR(50),
        home_scorer VARCHAR(255),
        home_scorer_id VARCHAR(50),
        home_assist VARCHAR(255),
        home_assist_id VARCHAR(50),
        away_scorer VARCHAR(255),
        away_scorer_id VARCHAR(50),
        away_assist VARCHAR(255),
        away_assist_id VARCHAR(50),
        score VARCHAR(10),
        info TEXT,
        score_info_time VARCHAR(50)
);

    CREATE TABLE Cards (
        id SERIAL PRIMARY KEY,
        match_id VARCHAR(50) REFERENCES Matches(match_id) ON DELETE CASCADE,
        time VARCHAR(50),
        home_fault VARCHAR(255),
        away_fault VARCHAR(255),
        card VARCHAR(50),
        home_player_id VARCHAR(50),
        away_player_id VARCHAR(50),
        score_info_time VARCHAR(50)
);

    CREATE TABLE Substitutions (
        id SERIAL PRIMARY KEY,
        match_id VARCHAR(50) REFERENCES Matches(match_id) ON DELETE CASCADE,
        time VARCHAR(50),
        substitution TEXT,
        substitution_player_id VARCHAR(50),
        team VARCHAR(10) CHECK (team IN ('home', 'away'))
);

    CREATE TABLE Lineups (
        id SERIAL PRIMARY KEY,
        match_id VARCHAR(50) REFERENCES Matches(match_id) ON DELETE CASCADE,
        player_name VARCHAR(255),
        lineup_number VARCHAR(50),
        lineup_position VARCHAR(50),
        team VARCHAR(10) CHECK (team IN ('home', 'away'))
);

    CREATE TABLE Statistics (
        id SERIAL PRIMARY KEY,
        match_id VARCHAR(50) REFERENCES Matches(match_id) ON DELETE CASCADE,
        type VARCHAR(50),
        home_value VARCHAR(50),
        away_value VARCHAR(50)
);

    CREATE TABLE FirstHalfStatistics (
        id SERIAL PRIMARY KEY,
        match_id VARCHAR(50) REFERENCES Matches(match_id) ON DELETE CASCADE,
        type VARCHAR(50),
        home_value VARCHAR(50),
        away_value VARCHAR(50)
);
    """)


def downgrade() -> None:
     op.execute("""
        DROP TABLE Players;
        DROP TABLE Venues;
        DROP TABLE Teams;
        DROP TABLE Competitions;
        DROP TABLE Countries;
    """)
