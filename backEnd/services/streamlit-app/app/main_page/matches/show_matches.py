import streamlit as st
import requests
import pandas as pd
import datetime

API_BASE_URL_MATCHES = "http://match-service:80/matches"
API_BASE_URL_BETTING = "http://betting-service:80/betts"
API_BASE_URL_ODDS = "http://match-service:80/odds"


def fetch_matches():
    try:
        response = requests.get(API_BASE_URL_MATCHES)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch matches: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching matches: {e}")
        return []

def fetch_odds(match_id):
    try:
        response = requests.get(f"{API_BASE_URL_ODDS}/{match_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch odds for Match ID {match_id}: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching odds: {e}")
        return None

def update_odds(match_id):
    try:
        response = requests.put(f"{API_BASE_URL_ODDS}/{match_id}")
        if response.status_code == 200:
            st.success(f"Odds updated successfully for Match ID {match_id}!")
        else:
            st.error(f"Failed to update odds for Match ID {match_id}: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred while updating odds: {e}")


def add_to_betting_list(match_id, home_team, away_team, user_id, home_coeff, away_coeff):    
    bet_payload = {
        "user_id": user_id,
        "match_id": match_id,
        "bet_type": "win",
        "selected_team": home_team,
        "amount": 1.0,
        "coefficient": home_coeff,
        "potential_win": 0.0,
        "status": "waiting_list"
    }


    try:
        response = requests.post(f"{API_BASE_URL_BETTING}/create-bet", json=bet_payload)
        if response.status_code in [200, 201]:
            st.success(f"The match has been successfully added to your betting list with default settings. You can modify the details in the Betts tab.")
        else:
            st.error(f"Failed to add Match ID {match_id} to betting list: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred while adding to the betting list: {e}")

def show_matches():
    
    user_id = st.session_state.get("user_id")
    
    st.title("Matches")

    matches = fetch_matches()
    if not matches:
        st.info("No matches available.")
        return

    df = pd.DataFrame(matches)
    df["match_date"] = pd.to_datetime(df["match_date"]).dt.strftime('%Y-%m-%d %H:%M:%S')

        # ==== filters ====
    st.sidebar.header("Filters")
    default_start_date = datetime.date(2024, 9, 17)
    start_date = st.sidebar.date_input("Start Date", value=default_start_date)
    end_date = st.sidebar.date_input("End Date")
    if start_date and end_date:
        filtered_dates = (df["match_date"] >= start_date.strftime('%Y-%m-%d')) & (df["match_date"] <= end_date.strftime('%Y-%m-%d'))
        df = df[filtered_dates]

    teams = pd.concat([df["home_team"], df["away_team"]]).unique()
    selected_team = st.sidebar.multiselect("Filter by team", teams)
    if selected_team:
        df = df[(df["home_team"].isin(selected_team)) | (df["away_team"].isin(selected_team))]

    # ==== sorting ====
    
    st.sidebar.header("Sorting")
    sort_by = st.sidebar.selectbox("Sort by", ["match_date"])
    sort_order = st.sidebar.radio("Sort order", ["Ascending", "Descending"])
    ascending = sort_order == "Ascending"

    df = df.sort_values(by=sort_by, ascending=ascending)

    # ==== show the list of matches ====
    for _, row in df.iterrows():
        with st.container():
            odds = fetch_odds(row["match_id"])
            if odds:
                odds_text = f"""
                <p><b>Odds:</b></p>
                <ul>
                    <li>Home Win: {odds['home_win']}</li>
                    <li>Draw: {odds['draw']}</li>
                    <li>Away Win: {odds['away_win']}</li>
                </ul>
                """
            else:
                odds_text = "<p><b>Odds:</b> Not available</p>"
            
            st.markdown(
                f"""
                <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
                    <h3>{row["home_team"]} vs {row["away_team"]}</h3>
                    <p><b>Date:</b> {row["match_date"]}</p>
                    {odds_text}
                </div>
                """,
                unsafe_allow_html=True,
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Add to betting list ({row['match_id']})", key=f"add_{row['match_id']}"):
                    add_to_betting_list(row["match_id"], row["home_team"], row["away_team"], user_id, row['home_coeff'], row['away_coeff'])
            with col2:
                if st.button(f"Update Odds ({row['match_id']})", key=f"update_{row['match_id']}"):
                    update_odds(row["match_id"])
                    st.rerun()