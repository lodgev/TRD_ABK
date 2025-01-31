import streamlit as st
import requests
import logging

# API URLs
API_BASE_URL_BETS = "http://betting-service:80/betts"
API_BASE_URL_MATCHES = "http://match-service:80/matches"
API_BASE_URL_ODDS = "http://match-service:80/odds"
API_BASE_URL_WALLET = "http://usage-service:80/wallet"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_match_details(match_id):
    try:
        response = requests.get(f"{API_BASE_URL_MATCHES}/{match_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch match details: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching match details: {e}")
        return None


def get_odds_for_match(match_id):
    try:
        response = requests.get(f"{API_BASE_URL_ODDS}/{match_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching odds: {e}")
        return None


def update_bet_status(bet_id, new_status):
    try:
        response = requests.put(f"{API_BASE_URL_BETS}/update-bet/{bet_id}", json={"status": new_status})
        if response.status_code == 200:
            st.success(f"Bet status updated to '{new_status}' successfully!")
        else:
            st.error(f"Failed to update bet status: {response.status_code} - {response.json().get('detail', '')}")
    except Exception as e:
        st.error(f"An error occurred while updating the bet: {e}")


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


def place_bet_page():
    st.title("Place Bet")

    selected_bet = st.session_state.get("selected_bet")
    if not selected_bet:
        st.warning("No bet selected.")
        st.button("Go Back", on_click=lambda: st.session_state.update({"current_page": "show_bets"}))
        st.rerun()
        return

    match_details = get_match_details(selected_bet["match_id"])
    if not match_details:
        st.warning("Match details could not be fetched.")
        st.button("Go Back", on_click=lambda: st.session_state.update({"current_page": "show_bets"}))
        st.rerun()
        return

    odds = get_odds_for_match(selected_bet["match_id"])
    if not odds:
        st.warning("Odds details could not be fetched.")
        st.button("Go Back", on_click=lambda: st.session_state.update({"current_page": "show_bets"}))
        st.rerun()
        return

    st.subheader("Bet Details")
    st.write(f"Match: {match_details['home_team']} vs {match_details['away_team']}")
    st.write(f"Match Date: {match_details['match_date']}")
    st.write(f"Created At: {selected_bet.get('created_at', 'N/A')}")

    # Display odds
    st.markdown(
        f"""
        <p><b>Odds:</b></p>
        <ul>
            <li>Home Win: {odds['home_win']}</li>
            <li>Draw: {odds['draw']}</li>
            <li>Away Win: {odds['away_win']}</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    # Select bet type and team
    bet_type = st.selectbox("Bet Type", ["win", "lose", "draw"], key="bet_type")
    selected_team = st.selectbox("Select Team", [match_details["home_team"], "Draw", match_details["away_team"]], key="selected_team")

    if selected_team == match_details["home_team"]:
        coefficient = odds["home_win"]
    elif selected_team == match_details["away_team"]:
        coefficient = odds["away_win"]
    else:  # Draw
        coefficient = odds["draw"]

    st.write(f"Coefficient: {coefficient}")

    # Input amount and calculate potential win
    amount = st.number_input("Bet Amount", min_value=1.0, value=selected_bet.get("amount", 1.0), step=1.0)
    potential_win = round(amount * coefficient, 2)
    st.write(f"Potential Win: {potential_win}")

    # Action buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Confirm"):
            wallet_response = requests.get(f"{API_BASE_URL_WALLET}/user/{st.session_state.user_id}")
            if wallet_response.status_code == 200:
                wallet_id = wallet_response.json().get("id")

                balance_response = update_wallet_balance(wallet_id, -amount)
                if balance_response:
                    st.success(f"Wallet updated. New balance: {balance_response['balance']} {balance_response['currency']}")

                    # Payload for updating the bet
                    bet_payload = {
                        "bet_type": bet_type,
                        "selected_team": selected_team,
                        "amount": amount,
                        "coefficient": coefficient,
                        "potential_win": potential_win,
                        "status": "pending"
                    }
                    try:
                        response = requests.put(f"{API_BASE_URL_BETS}/update-bet/{selected_bet['bet_id']}", json=bet_payload)
                        if response.status_code == 200:
                            st.success("Bet placed successfully! Status updated to 'pending'.")
                            st.session_state["current_page"] = "show_bets"
                            st.rerun()
                        else:
                            st.error(f"Failed to update bet: {response.status_code} - {response.json().get('detail', '')}")
                    except Exception as e:
                        st.error(f"An error occurred while updating the bet: {e}")
                else:
                    st.error("Failed to update wallet balance.")
            else:
                st.error("Failed to fetch wallet information.")

    with col2:
        if st.button("Cancel"):
            update_bet_status(selected_bet["bet_id"], "waiting_list")
            st.session_state["current_page"] = "show_bets"
            st.rerun()

    with col3:
        if st.button("Back"):
            st.session_state["current_page"] = "show_bets"
            st.rerun()

