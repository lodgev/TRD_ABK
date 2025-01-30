import streamlit as st
import requests
import pandas as pd
import logging

# API URLs
API_BASE_URL_BETS = "http://betting-service:80/betts"
API_BASE_URL_ODDS = "http://match-service:80/odds"

# Логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальный кэш для odds
odds_cache = {}


def fetch_bets(user_id):
    """Получает все ставки пользователя."""
    try:
        response = requests.get(f"{API_BASE_URL_BETS}/get-all-bets")
        if response.status_code == 200:
            bets = response.json()
            return [bet for bet in bets if bet["user_id"] == user_id]
        else:
            st.error(f"Failed to fetch bets: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching bets: {e}")
        return []


def fetch_all_odds():
    """Получает все коэффициенты (odds) и сохраняет в кэше."""
    global odds_cache
    try:
        response = requests.get(f"{API_BASE_URL_ODDS}/")
        if response.status_code == 200:
            odds_list = response.json()
            # Сохраняем odds в кэше (по match_id)
            odds_cache = {odds["match_id"]: odds for odds in odds_list}
            logger.info("Successfully fetched all odds")
        else:
            logger.warning(f"Failed to fetch all odds: {response.status_code}")
            odds_cache = {}
    except Exception as e:
        st.error(f"An error occurred while fetching odds: {e}")
        odds_cache = {}


def get_odds_for_match(match_id):
    """Получает коэффициенты из кэша, если они там есть."""
    return odds_cache.get(match_id, None)


def delete_bet(bet_id):
    """Удаляет ставку."""
    try:
        response = requests.delete(f"{API_BASE_URL_BETS}/cancel-bet/{bet_id}")
        if response.status_code == 200:
            st.success(f"Bet ID {bet_id} deleted successfully!")
        else:
            st.error(f"Failed to delete bet: {response.status_code} - {response.json().get('detail', '')}")
    except Exception as e:
        st.error(f"An error occurred while deleting the bet: {e}")


def show_bets():
    """Отображает список ставок."""
    st.title("My Bets")
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("You need to log in to view your bets.")
        return

    bets = fetch_bets(user_id)

    if not bets:
        st.info("No bets available.")
        return

    # Загружаем все odds перед отображением
    fetch_all_odds()

    df = pd.DataFrame(bets)
    tabs = st.tabs(["Betting Attent", "Betting In Course", "History"])

    # **Betting Attent: status = waiting_list**
    with tabs[0]:
        st.header("Betting Attent")
        attent_bets = df[df["status"] == "waiting_list"]
        if attent_bets.empty:
            st.write("No bets in the waiting list.")
        else:
            for _, row in attent_bets.iterrows():
                with st.container():
                    odds = get_odds_for_match(row["match_id"])
                    odds_text = (
                        f"<p><b>Odds:</b> Home Win: {odds['home_win']}, Draw: {odds['draw']}, Away Win: {odds['away_win']}</p>"
                        if odds
                        else "<p><b>Odds:</b> Not available</p>"
                    )

                    st.markdown(
                        f"""
                        <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
                            <h3>{row['selected_team']} ({row['bet_type']})</h3>
                            {odds_text}
                            <p><b>Amount:</b> {row['amount']}</p>
                            <p><b>Potential Win:</b> {row['potential_win']}</p>
                            <p><b>Status:</b> {row['status']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Place Bet (ID: {row['bet_id']})", key=f"place-{row['bet_id']}"):
                            st.session_state["selected_bet"] = row.to_dict()
                            st.session_state["current_page"] = "place_bet"
                            st.rerun()
                    with col2:
                        if st.button(f"Remove (ID: {row['bet_id']})", key=f"remove-{row['bet_id']}"):
                            delete_bet(row["bet_id"])
                            st.rerun()

    # **Betting In Course: status = pending**
    with tabs[1]:
        st.header("Betting In Course")
        in_course_bets = df[df["status"] == "pending"]
        if in_course_bets.empty:
            st.write("No bets in course.")
        else:
            for _, row in in_course_bets.iterrows():
                with st.container():
                    odds = get_odds_for_match(row["match_id"])
                    odds_text = (
                        f"<p><b>Odds:</b> Home Win: {odds['home_win']}, Draw: {odds['draw']}, Away Win: {odds['away_win']}</p>"
                        if odds
                        else "<p><b>Odds:</b> Not available</p>"
                    )

                    st.markdown(
                        f"""
                        <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
                            <h3>{row['selected_team']} ({row['bet_type']})</h3>
                            {odds_text}
                            <p><b>Match ID:</b> {row['match_id']}</p>
                            <p><b>Amount:</b> {row['amount']}</p>
                            <p><b>Potential Win:</b> {row['potential_win']}</p>
                            <p><b>Status:</b> {row['status']}</p>
                            <p><b>Created At:</b> {row['created_at']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button(f"Cancel Bet (ID: {row['bet_id']})", key=f"cancel-{row['bet_id']}"):
                        delete_bet(row["bet_id"])
                        st.rerun()

    # **History: status = won or lost**
    with tabs[2]:
        st.header("History")
        history_bets = df[df["status"].isin(["won", "lost"])]
        if history_bets.empty:
            st.write("No betting history available.")
        else:
            for _, row in history_bets.iterrows():
                odds = get_odds_for_match(row["match_id"])
                odds_text = (
                    f"<p><b>Odds:</b> Home Win: {odds['home_win']}, Draw: {odds['draw']}, Away Win: {odds['away_win']}</p>"
                    if odds
                    else "<p><b>Odds:</b> Not available</p>"
                )

                st.markdown(
                    f"""
                    <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
                        <h3>{row['selected_team']} ({row['bet_type']})</h3>
                        {odds_text}
                        <p><b>Match ID:</b> {row['match_id']}</p>
                        <p><b>Amount:</b> {row['amount']}</p>
                        <p><b>Potential Win:</b> {row['potential_win']}</p>
                        <p><b>Status:</b> {row['status']}</p>
                        <p><b>Created At:</b> {row['created_at']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # **Betting Attent: status = waiting_list**
    # with tabs[0]:
    #     st.header("Betting Attent")
    #     attent_bets = df[df["status"] == "waiting_list"]
    #     if attent_bets.empty:
    #         st.write("No bets in the waiting list.")
    #     else:
    #         for _, row in attent_bets.iterrows():
    #             with st.container():
    #                 odds = fetch_odds(row["match_id"])
    #                 odds_text = (
    #                     f"<p><b>Odds:</b> Home Win: {odds['home_win']}, Draw: {odds['draw']}, Away Win: {odds['away_win']}</p>"
    #                     if odds
    #                     else "<p><b>Odds:</b> Not available</p>"
    #                 )
    #                 st.markdown(
    #                     f"""
    #                     <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
    #                         <h3>{row['selected_team']} ({row['bet_type']})</h3>
    #                         {odds_text}
    #                         <p><b>Amount:</b> {row['amount']}</p>
    #                         <p><b>Potential Win:</b> {row['potential_win']}</p>
    #                         <p><b>Status:</b> {row['status']}</p>
    #                     </div>
    #                     """,
    #                     unsafe_allow_html=True,
    #                 )
    #                 col1, col2 = st.columns(2)
    #                 with col1:
    #                     if st.button(f"Place Bet (ID: {row['bet_id']})", key=f"place-{row['bet_id']}"):
    #                         # Save the selected bet to session state and navigate to place_bet page
    #                         st.session_state["selected_bet"] = row.to_dict()
    #                         st.session_state["current_page"] = "place_bet"
    #                         st.rerun()
    #                 with col2:
    #                     if st.button(f"Remove (ID: {row['bet_id']})", key=f"remove-{row['bet_id']}"):
    #                         delete_bet(row["bet_id"])
    #                         st.rerun()
    #
    # # **Betting In Course: status = pending**
    # with tabs[1]:
    #     st.header("Betting In Course")
    #     in_course_bets = df[df["status"] == "pending"]
    #     if in_course_bets.empty:
    #         st.write("No bets in course.")
    #     else:
    #         for _, row in in_course_bets.iterrows():
    #             with st.container():
    #                 st.markdown(
    #                     f"""
    #                     <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
    #                         <h3>{row['selected_team']} ({row['bet_type']})</h3>
    #                         <p><b>Match ID:</b> {row['match_id']}</p>
    #                         <p><b>Amount:</b> {row['amount']}</p>
    #                         <p><b>Potential Win:</b> {row['potential_win']}</p>
    #                         <p><b>Status:</b> {row['status']}</p>
    #                         <p><b>Created At:</b> {row['created_at']}</p>
    #                     </div>
    #                     """,
    #                     unsafe_allow_html=True,
    #                 )
    #                 if st.button(f"Cancel Bet (ID: {row['bet_id']})", key=f"cancel-{row['bet_id']}"):
    #                     delete_bet(row["bet_id"])
    #                     st.rerun()
    #
    # # **History: status = won or lost**
    # with tabs[2]:
    #     st.header("History")
    #     history_bets = df[df["status"].isin(["won", "lost"])]
    #     if history_bets.empty:
    #         st.write("No betting history available.")
    #     else:
    #         for _, row in history_bets.iterrows():
    #             st.markdown(
    #                 f"""
    #                 <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
    #                     <h3>{row['selected_team']} ({row['bet_type']})</h3>
    #                     <p><b>Match ID:</b> {row['match_id']}</p>
    #                     <p><b>Amount:</b> {row['amount']}</p>
    #                     <p><b>Potential Win:</b> {row['potential_win']}</p>
    #                     <p><b>Status:</b> {row['status']}</p>
    #                     <p><b>Created At:</b> {row['created_at']}</p>
    #                 </div>
    #                 """,
    #                 unsafe_allow_html=True,
    #             )
