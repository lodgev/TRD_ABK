import streamlit as st
import requests
import pandas as pd
import logging

# API URLs
API_BASE_URL_BETS = "http://betting-service:80/betts"
API_BASE_URL_ODDS = "http://match-service:80/odds"
API_BASE_URL_WALLET = "http://usage-service:80/wallet"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def fetch_odds(match_id):
    """Получает коэффициенты (odds) для матча."""
    try:
        response = requests.get(f"{API_BASE_URL_ODDS}/{match_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching odds: {e}")
        return None

def update_wallet_balance(wallet_id, amount):
    try:
        response = requests.put(
            f"{API_BASE_URL_WALLET}/{wallet_id}/update-balance",
            json={"amount": amount}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to update wallet balance: {response.status_code} - {response.json().get('detail', '')}")
            return None
    except Exception as e:
        st.error(f"An error occurred while updating wallet balance: {e}")
        return None

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
    st.title("My Bets")
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("You need to log in to view your bets.")
        return

    bets = fetch_bets(user_id)
    if not bets:
        st.info("No bets available.")
        return

    df = pd.DataFrame(bets)
    selected_bets = []  # Store selected bets for combined bet

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
                    odds = fetch_odds(row["match_id"])
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

                    # Option to select the bet for combined bet
                    selected = st.checkbox(f"Select for Combined Bet (ID: {row['bet_id']})", key=f"select-{row['bet_id']}")
                    if selected:
                        selected_bets.append(row.to_dict())

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

    if selected_bets:
        if st.button("Create Combined Bet"):
            st.session_state["selected_combined_bets"] = selected_bets
            st.session_state["current_page"] = "place_combined_bet"
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
                    odds = fetch_odds(row["match_id"])
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
                        wallet_response = requests.get(f"{API_BASE_URL_WALLET}/user/{st.session_state.user_id}")
                        if wallet_response.status_code == 200:
                            wallet_id = wallet_response.json().get("id")

                            refund_response = update_wallet_balance(wallet_id, row['amount'])
                            if refund_response:
                                st.success(
                                    f"Wallet refunded. New balance: {refund_response['balance']} {refund_response['currency']}")

                                delete_bet(row["bet_id"])
                                st.rerun()
                            else:
                                st.error("Failed to refund wallet balance.")
                        else:
                            st.error("Failed to fetch wallet information.")


    # **History: status = won or lost**
    with tabs[2]:
        st.header("History")
        history_bets = df[df["status"].isin(["won", "lost"])]
        if history_bets.empty:
            st.write("No betting history available.")
        else:
            for _, row in history_bets.iterrows():
                odds = fetch_odds(row["match_id"])
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
