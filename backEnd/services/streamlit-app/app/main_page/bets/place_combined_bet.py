import streamlit as st
import requests
import logging

# API URLs
API_BASE_URL_BETS = "http://betting-service:80/betts"
API_BASE_URL_BETS_COMB = "http://betting-service:80/combined-betts"
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

def update_wallet_balance(wallet_id, amount):
    try:
        response = requests.put(f"{API_BASE_URL_WALLET}/{wallet_id}/update-balance", json={"amount": amount})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to update wallet balance: {response.status_code} - {response.json().get('detail', '')}")
            return None
    except Exception as e:
        st.error(f"An error occurred while updating wallet balance: {e}")
        return None

def update_bet_status_to_pending(bet_id):
    """Updates the status of a bet to 'pending'."""
    try:
        response = requests.put(f"{API_BASE_URL_BETS}/update-bet/{bet_id}", json={"status": "pending"})
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to update bet status: {response.status_code} - {response.json().get('detail', '')}")
            return False
    except Exception as e:
        st.error(f"An error occurred while updating the bet status: {e}")
        return False

def place_combined_bet_page():
    """Page to handle placing a combined bet."""
    st.title("Place Combined Bet")

    selected_combined_bets = st.session_state.get("selected_combined_bets")
    if not selected_combined_bets:
        st.warning("No bets selected for a combined bet.")
        st.button("Go Back", on_click=lambda: st.session_state.update({"current_page": "show_bets"}))
        st.rerun()
        return

    st.subheader("Selected Bets")
    total_coefficient = 1.0
    valid_bets = []
    seen_bets = {"matches": set(), "teams": set()}

    for idx, bet in enumerate(selected_combined_bets):
        match_details = get_match_details(bet["match_id"])
        odds = get_odds_for_match(bet["match_id"])

        if not match_details or not odds:
            st.error(f"Failed to retrieve match or odds details for match ID {bet['match_id']}.")
            continue

        st.divider()
        st.subheader(f"Bet Details ({idx + 1})")
        st.write(f"Match: {match_details['home_team']} vs {match_details['away_team']}")
        st.write(f"Match Date: {match_details['match_date']}")
        st.write(f"Created At: {bet.get('created_at', 'N/A')}")

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


        # Display match and odds details
        selected_team = st.selectbox(
            f"Select Team (Bet {idx + 1})",
            [match_details["home_team"], "Draw", match_details["away_team"]],
            key=f"selected_team_{idx}"
        )

        if bet["match_id"] in seen_bets["matches"]:
            st.error(f"Duplicate bet detected: You already have a bet on match ID {bet['match_id']}.")
            continue

        if selected_team in seen_bets["teams"]:
            st.error(f"Duplicate bet detected: You already have a bet on the team '{selected_team}'.")
            continue

            # Add to tracking sets
        seen_bets["matches"].add(bet["match_id"])
        seen_bets["teams"].add(selected_team)

        coefficient = (
            odds["home_win"] if selected_team == match_details["home_team"]
            else odds["away_win"] if selected_team == match_details["away_team"]
            else odds["draw"]
        )

        st.write(f"Coefficient: {coefficient}")

        total_coefficient *= coefficient
        bet_type = st.selectbox(
            f"Bet Type (Bet {idx + 1})",
            ["win", "lose", "draw"],
            key=f"bet_type_{idx}"
        )

        valid_bets.append({
            "match_id": bet["match_id"],
            "bet_id": bet["bet_id"],  # Track bet ID to update status later
            "bet_type": bet_type,
            "selected_team": selected_team,
            "coefficient": coefficient
        })

    if not valid_bets:
        st.warning("No valid bets available for a combined bet.")
        return

    st.divider()
    total_amount = st.number_input("Total Amount for Combined Bet", min_value=1.0, step=1.0)
    potential_win = round(total_amount * total_coefficient, 2)
    st.write(f"Total Coefficient: {total_coefficient}")
    st.write(f"Potential Win: {potential_win}")

    # Confirm or cancel the combined bet
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Confirm Combined Bet"):
            wallet_response = requests.get(f"{API_BASE_URL_WALLET}/user/{st.session_state.user_id}")
            if wallet_response.status_code == 200:
                wallet_id = wallet_response.json().get("id")

                balance_response = update_wallet_balance(wallet_id, -total_amount)
                if balance_response:
                    st.success(f"Wallet updated. New balance: {balance_response['balance']} {balance_response['currency']}")

                    combined_bet_payload = {
                        "user_id": st.session_state.user_id,
                        "total_amount": total_amount,
                        "details": valid_bets
                    }

                    try:
                        response = requests.post(f"{API_BASE_URL_BETS_COMB}/create-combined-bet", json=combined_bet_payload)
                        if response.status_code in [200, 201]:
                            st.success("Combined bet placed successfully!")

                            # Update the status of each individual bet to "pending"
                            for bet in valid_bets:
                                update_bet_status_to_pending(bet["bet_id"])

                            st.session_state["current_page"] = "show_bets"
                            st.rerun()
                        else:
                            st.error(f"Failed to create combined bet: {response.status_code} - {response.json().get('detail', '')}")
                    except Exception as e:
                        st.error(f"An error occurred while creating the combined bet: {e}")
                else:
                    st.error("Failed to update wallet balance.")
            else:
                st.error("Failed to fetch wallet information.")

    with col2:
        if st.button("Back"):
            st.session_state["current_page"] = "show_bets"
            st.rerun()


#
# def place_combined_bet_page():
#     st.title("Place Combined Bet")
#
#     selected_combined_bets = st.session_state.get("selected_combined_bets")
#     if not selected_combined_bets:
#         st.warning("No bets selected for a combined bet.")
#         st.button("Go Back", on_click=lambda: st.session_state.update({"current_page": "show_bets"}))
#         st.rerun()
#         return
#
#     st.subheader("Selected Bets")
#     for bet in selected_combined_bets:
#         st.markdown(
#             f"""
#             <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
#                 <h3>{bet['selected_team']} ({bet['bet_type']})</h3>
#                 <p><b>Match ID:</b> {bet['match_id']}</p>
#                 <p><b>Coefficient:</b> {bet['coefficient']}</p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#
#     total_amount = st.number_input("Total Amount for Combined Bet", min_value=1.0, step=1.0)
#
#     if st.button("Confirm Combined Bet"):
#         combined_bet_data = {
#             "user_id": st.session_state.user_id,
#             "total_amount": total_amount,
#             "details": [
#                 {
#                     "match_id": bet["match_id"],
#                     "bet_type": bet["bet_type"],
#                     "selected_team": bet["selected_team"],
#                     "coefficient": bet["coefficient"],
#                 }
#                 for bet in selected_combined_bets
#             ],
#         }
#
#         # Send a request to create the combined bet
#         response = requests.post(f"{API_BASE_URL_BETS}/create-combined-bet", json=combined_bet_data)
#         if response.status_code in [200, 201]:
#             st.success("Combined bet placed successfully!")
#             st.session_state["current_page"] = "show_bets"
#             st.rerun()
#         else:
#             st.error(f"Failed to place combined bet: {response.status_code} - {response.json().get('detail', '')}")
#
#     if st.button("Back"):
#         st.session_state["current_page"] = "show_bets"
#         st.rerun()