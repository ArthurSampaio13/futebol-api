import streamlit as st
import psycopg2
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

import warnings
warnings.filterwarnings("ignore")

load_dotenv()

st.set_page_config(page_title="Football Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("<div id='top'></div>", unsafe_allow_html=True);

st.markdown(
    """
    <style>
    .main {
        background-color: #ffffff;
    }
    .stApp {
        color: #333333;
        font-family: Arial, sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        background-color: #f9f9f9;
    }
    .card img {
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .card h4 {
        margin: 0;
    }
    .card p {
        margin: 5px 0;
        font-size: 14px;
        color: #666;
    }
    .score {
        font-size: 20px;
        font-weight: bold;
    }
    .team-logo {
        width: 60px;
        height: 60px;
        border-radius: 50%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_connection():
    return psycopg2.connect(DB_URL)

def query_db(query, params=None):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def query_db_with_pagination(query, page, items_per_page):
    conn = get_connection()
    offset = (page - 1) * items_per_page
    paginated_query = f"{query} OFFSET {offset} LIMIT {items_per_page};"
    df = pd.read_sql(paginated_query, conn)
    conn.close()
    return df

ITEMS_PER_PAGE = 5

if "page" not in st.session_state:
    st.session_state.page = 1

st.sidebar.title("Navegação")
section = st.sidebar.radio("Ir para:", ("Times", "Países", "Jogos Recentes", "Estatísticas de Jogadores"))

if section == "Times":
    st.title("Times")
    teams_query = "SELECT team_key, team_name, team_country, team_founded, team_badge FROM Teams;"
    teams_data = query_db(teams_query)
    if not teams_data.empty:
        selected_team = st.selectbox("Selecione um time:", teams_data['team_name'].unique())
        selected_team_data = teams_data[teams_data['team_name'] == selected_team]
        st.markdown(
            f"""
            <div class="card">
                <h4>{selected_team_data.iloc[0]['team_name']}</h4>
                <p><strong>País:</strong> {selected_team_data.iloc[0]['team_country']}</p>
                <p><strong>Fundado em:</strong> {selected_team_data.iloc[0]['team_founded']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if selected_team_data.iloc[0]['team_badge']:
            st.image(selected_team_data.iloc[0]['team_badge'], width=150, caption="Logo do Time")

elif section == "Países":
    st.title("Países")
    countries_query = "SELECT country_id, country_name, country_logo FROM Countries;"
    countries_data = query_db(countries_query)
    if not countries_data.empty:
        selected_country = st.selectbox("Selecione um país:", countries_data['country_name'].unique())
        selected_country_data = countries_data[countries_data['country_name'] == selected_country]
        st.markdown(
            f"""
            <div class="card">
                <h4>{selected_country_data.iloc[0]['country_name']}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        if selected_country_data.iloc[0]['country_logo']:
            st.image(selected_country_data.iloc[0]['country_logo'], width=150, caption="Logo do País")

if section == "Jogos Recentes":
    st.title("Jogos Recentes")
    matches_query = """
        SELECT match_id, match_date, match_hometeam_name, match_hometeam_score, match_awayteam_name, match_awayteam_score, 
               team_home_badge, team_away_badge, match_stadium, match_referee, match_hometeam_halftime_score,
               match_awayteam_halftime_score, match_hometeam_extra_score, match_awayteam_extra_score, 
               match_hometeam_penalty_score, match_awayteam_penalty_score, match_hometeam_system, match_awayteam_system
        FROM Matches
        ORDER BY match_date DESC
    """
    matches_data = query_db_with_pagination(matches_query, st.session_state.page, ITEMS_PER_PAGE)

    if not matches_data.empty:
        for _, match in matches_data.iterrows():
            st.markdown(
                f"""
                <div class="card">
                    <div style="display: flex; align-items: center;">
                        <div style="flex: 1; text-align: center;">
                            <img src="{match['team_home_badge']}" width="60" height="60" style="border-radius: 50%;" alt="Logo do Time Casa">
                            <p>{match['match_hometeam_name']}</p>
                        </div>
                        <div style="flex: 1; text-align: center;">
                            <p class="stat">{match['match_hometeam_score']} - {match['match_awayteam_score']}</p>
                            <p>{datetime.strptime(match['match_date'], '%Y-%m-%d').strftime('%d %b %Y')}</p>
                        </div>
                        <div style="flex: 1; text-align: center;">
                            <img src="{match['team_away_badge']}" width="60" height="60" style="border-radius: 50%;" alt="Logo do Time Visitante">
                            <p>{match['match_awayteam_name']}</p>
                        </div>
                    </div>
                    <hr>
                    <p><strong>Estádio:</strong> {match['match_stadium']}</p>
                    <p><strong>Árbitro:</strong> {match['match_referee']}</p>
                    <p>Placar no Intervalo: {match['match_hometeam_halftime_score']} - {match['match_awayteam_halftime_score']}</p>
                    <p>Placar no Tempo Extra: {match['match_hometeam_extra_score']} - {match['match_awayteam_extra_score']}</p>
                    <p>Placar nos Pênaltis: {match['match_hometeam_penalty_score']} - {match['match_awayteam_penalty_score']}</p>
                    <p><strong>Formação Time da Casa:</strong> {match['match_hometeam_system']}</p>
                    <p><strong>Formação Time Visitante:</strong> {match['match_awayteam_system']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander(f"Goleadores - {match['match_hometeam_name']} x {match['match_awayteam_name']}"):
                goalscorers_query = "SELECT time, home_scorer, away_scorer, score FROM Goalscorers WHERE match_id = %s"
                goalscorers = query_db(goalscorers_query, (match['match_id'],))
                if not goalscorers.empty:
                    for _, scorer in goalscorers.iterrows():
                        st.write(f"Tempo: {scorer['time']} - {scorer['home_scorer'] if scorer['home_scorer'] else scorer['away_scorer']} ({scorer['score']})")
                else:
                    st.write("Nenhum goleador registrado.")

            with st.expander(f"Cartões - {match['match_hometeam_name']} x {match['match_awayteam_name']}"):
                cards_query = "SELECT time, home_fault, away_fault, card FROM Cards WHERE match_id = %s"
                cards = query_db(cards_query, (match['match_id'],))
                if not cards.empty:
                    for _, card in cards.iterrows():
                        st.write(f"Tempo: {card['time']} - {card['home_fault'] or card['away_fault']} ({card['card']})")
                else:
                    st.write("Nenhum cartão registrado.")

            with st.expander(f"Substituições - {match['match_hometeam_name']} x {match['match_awayteam_name']}"):
                substitutions_query = "SELECT time, substitution, team FROM Substitutions WHERE match_id = %s"
                substitutions = query_db(substitutions_query, (match['match_id'],))
                if not substitutions.empty:
                    for _, sub in substitutions.iterrows():
                        st.write(f"Tempo: {sub['time']} - {sub['substitution']} ({'Casa' if sub['team'] == 'home' else 'Visitante'})")
                else:
                    st.write("Nenhuma substituição registrada.")

            with st.expander(f"Estatísticas da Partida - {match['match_hometeam_name']} x {match['match_awayteam_name']}"):
                statistics_query = "SELECT type, home_value, away_value FROM Statistics WHERE match_id = %s"
                statistics = query_db(statistics_query, (match['match_id'],))
                if not statistics.empty:
                    for _, stat in statistics.iterrows():
                        st.write(f"{stat['type']}: {stat['home_value']} - {stat['away_value']}")
                else:
                    st.write("Nenhuma estatística registrada.")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("Página Anterior") and st.session_state.page > 1:
                st.session_state.page -= 1
        with col3:
            if st.button("Próxima Página"):
                st.session_state.page = 1 if st.session_state.page == ITEMS_PER_PAGE else st.session_state.page + 1

elif section == "Estatísticas de Jogadores":
    st.title("Estatísticas de Jogadores")
    players_query = """
        SELECT player_id, player_name, player_complete_name, player_number, player_country, player_type, 
               player_age, player_match_played, player_goals, player_yellow_cards, player_red_cards, 
               player_injured, player_substitute_out, player_substitutes_on_bench, player_assists, 
               player_is_captain, player_rating, player_image, player_goals_conceded, player_fouls_committed
        FROM Players;
    """
    players_data = query_db(players_query)
    if not players_data.empty:
        selected_player = st.selectbox("Selecione um jogador:", players_data['player_name'].unique())
        player_data = players_data[players_data['player_name'] == selected_player].iloc[0]
        st.markdown(
            f"""
            <div class="card" style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 2;">
                    <h4>{player_data['player_complete_name']} (#{player_data['player_number']})</h4>
                    <p><strong>Posição:</strong> {player_data['player_type']}</p>
                    <p><strong>Idade:</strong> {player_data['player_age']}</p>
                    <p class="stat">Partidas Jogadas: {player_data['player_match_played']}</p>
                    <p class="stat">Gols: {player_data['player_goals']}</p>
                    <p class="stat">Assistências: {player_data['player_assists']}</p>
                    <p class="stat">Faltas realizadas: {player_data['player_fouls_committed']}</p>
                    <p class="stat">Cartões Amarelos: {player_data['player_yellow_cards']}</p>
                    <p class="stat">Cartões Vermelhos: {player_data['player_red_cards']}</p>
                    <p><strong>Lesionado:</strong> {player_data['player_injured']}</p>
                    <p><strong>Capitão:</strong> {player_data['player_is_captain']}</p>
                    <p><strong>Nota do Jogador:</strong> {player_data['player_rating']}</p>
                </div>
                <div style="flex: 1; text-align: right;">
                    <img src="{player_data['player_image']}" width="120" height="120" style="border-radius: 50%;" alt="Imagem do jogador">
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    """
    <style>
    .float-button {
        position: fixed;
        width: 50px;
        height: 50px;
        bottom: 40px;
        right: 40px;
        background-color: #3498db;
        color: white;
        border-radius: 50px;
        text-align: center;
        font-size: 22px;
        box-shadow: 2px 2px 3px rgba(0, 0, 0, 0.3);
        z-index: 1000;
    }
    .float-button:hover {
        background-color: #2980b9;
    }
    </style>
    <a href="#top" class="float-button">⬆️</a>
    """,
    unsafe_allow_html=True
)