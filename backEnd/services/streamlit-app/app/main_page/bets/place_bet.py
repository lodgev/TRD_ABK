# # import streamlit as st
# # import requests

# # API_BASE_URL_BETTING = "http://betting-service:80/betts"
# # API_BASE_URL_MATCHES = "http://match-service:80/matches"

# # def get_match_details(match_id):
# #     """Fetch match details from the match service."""
# #     try:
# #         response = requests.get(f"{API_BASE_URL_MATCHES}/{match_id}")
# #         if response.status_code == 200:
# #             return response.json()
# #         else:
# #             st.error(f"Failed to fetch match details: {response.status_code}")
# #             return None
# #     except Exception as e:
# #         st.error(f"An error occurred while fetching match details: {e}")
# #         return None

# # def update_bet_status(bet_id, new_status):
# #     """Update the status of a bet."""
# #     try:
# #         response = requests.put(f"{API_BASE_URL_BETTING}/update-bet/{bet_id}", json={"status": new_status})
# #         if response.status_code == 200:
# #             st.success(f"Bet status updated to '{new_status}' successfully!")
# #         else:
# #             st.error(f"Failed to update bet status: {response.status_code} - {response.json().get('detail', '')}")
# #     except Exception as e:
# #         st.error(f"An error occurred while updating the bet: {e}")

# # def place_bet_page():
# #     st.title("Place Bet")

# #     selected_bet = st.session_state.get("selected_bet")
# #     if not selected_bet:
# #         st.warning("No bet selected.")
# #         st.button("Go Back", on_click=lambda: st.session_state.update({"current_page": "show_bets"}))
# #         st.rerun()
# #         return

# #     # Fetch match details
# #     match_details = get_match_details(selected_bet["match_id"])
# #     if not match_details:
# #         st.warning("Unable to fetch match details.")
# #         st.button("Go Back", on_click=lambda: st.session_state.update({"current_page": "show_bets"}))
# #         st.rerun()
# #         return

# #     # Add match details to the selected bet
# #     selected_bet["home_team"] = match_details["home_team"]
# #     selected_bet["away_team"] = match_details["away_team"]

# #     # Display the bet details
# #     st.subheader("Bet Details")
# #     st.write(f"Match: {selected_bet['home_team']} vs {selected_bet['away_team']}")
# #     st.write(f"Selected Team: {selected_bet['selected_team']}")
# #     st.write(f"Bet Type: {selected_bet['bet_type']}")
# #     st.write(f"Amount: {selected_bet['amount']}")
# #     st.write(f"Potential Win: {selected_bet['potential_win']}")
# #     st.write(f"Created At: {selected_bet['created_at']}")

# #     # Form for user input
# #     st.subheader("Edit Bet Details")
# #     selected_bet["selected_team"] = st.selectbox(
# #         "Select Team",
# #         [selected_bet["home_team"], selected_bet["away_team"]],
# #         index=0 if selected_bet["selected_team"] == selected_bet["home_team"] else 1
# #     )
# #     selected_bet["amount"] = st.number_input("Amount", min_value=0.0, value=selected_bet["amount"])
# #     selected_bet["potential_win"] = selected_bet["amount"] * selected_bet["coefficient"]

# #     col1, col2, col3 = st.columns(3)
# #     with col1:
# #         if st.button("Confirm"):
# #             update_bet_status(selected_bet["bet_id"], "pending")
# #             st.session_state["current_page"] = "show_bets"
# #             st.rerun()

# #     with col2:
# #         if st.button("Cancel"):
# #             update_bet_status(selected_bet["bet_id"], "waiting_list")
# #             st.session_state["current_page"] = "show_bets"
# #             st.rerun()

# #     with col3:
# #         if st.button("Back"):
# #             st.session_state["current_page"] = "show_bets"
# #             st.rerun()

import streamlit as st
import requests

API_BASE_URL = "http://betting-service:80/betts"
API_MATCH_BASE_URL = "http://match-service:80/matches"

def get_match_details(match_id):
    """Fetch match details by match ID."""
    try:
        response = requests.get(f"{API_MATCH_BASE_URL}/{match_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch match details: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching match details: {e}")
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

    st.subheader("Bet Details")
    st.write(f"Match: {match_details['home_team']} vs {match_details['away_team']}")
    st.write(f"Match Date: {match_details['match_date']}")

    # Team selection
    selected_team = st.selectbox("Select Team", [match_details["home_team"], match_details["away_team"]])

    # Get coefficient based on selected team
    if selected_team == match_details["home_team"]:
        coefficient = match_details["home_coeff"]
    else:
        coefficient = match_details["away_coeff"]

    st.write(f"Coefficient: {coefficient}")

    # Amount input
    amount = st.number_input("Bet Amount", min_value=1.0, value=selected_bet.get("amount", 1.0), step=1.0)

    # Calculate potential win
    potential_win = round(amount * coefficient, 2)
    st.write(f"Potential Win: {potential_win}")

    # Bet Type
    bet_type = st.selectbox("Bet Type", ["win", "lose", "draw"])

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Confirm"):
            # Update the bet details in the database
            bet_payload = {
                "user_id": selected_bet["user_id"],
                "match_id": selected_bet["match_id"],
                "bet_type": bet_type,
                "selected_team": selected_team,
                "amount": amount,
                "coefficient": coefficient,
                "potential_win": potential_win,
                "status": "pending"
            }
            try:
                response = requests.post(f"{API_BASE_URL}/create-bet", json=bet_payload)
                if response.status_code == 201:
                    st.success("Bet placed successfully!")
                    st.session_state["current_page"] = "show_bets"
                    st.rerun()
                else:
                    st.error(f"Failed to place bet: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred while placing the bet: {e}")

    with col2:
        if st.button("Cancel"):
            st.session_state["current_page"] = "show_bets"
            st.rerun()

    with col3:
        if st.button("Back"):
            st.session_state["current_page"] = "show_bets"
            st.rerun()


# import streamlit as st
# import requests

# API_BASE_URL_BETTING = "http://betting-service:80/betts"
# API_BASE_URL_MATCHES = "http://match-service:80/matches"

# def get_match_details(match_id):
#     """Fetch match details from the match service."""
#     try:
#         response = requests.get(f"{API_BASE_URL_MATCHES}/{match_id}")
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.error(f"Failed to fetch match details: {response.status_code}")
#             return None
#     except Exception as e:
#         st.error(f"An error occurred while fetching match details: {e}")
#         return None

# def update_bet_status(bet_id, new_status):
#     """Update the status of a bet."""
#     try:
#         response = requests.put(f"{API_BASE_URL_BETTING}/update-bet/{bet_id}", json={"status": new_status})
#         if response.status_code == 200:
#             st.success(f"Bet status updated to '{new_status}' successfully!")
#         else:
#             st.error(f"Failed to update bet status: {response.status_code} - {response.json().get('detail', '')}")
#     except Exception as e:
#         st.error(f"An error occurred while updating the bet: {e}")

# def place_bet_page():
#     st.title("Place Bet")

#     selected_bet = st.session_state.get("selected_bet")
#     if not selected_bet:
#         st.warning("No bet selected.")
#         st.button("Go Back", on_click=lambda: st.session_state.update({"current_page": "show_bets"}))
#         st.rerun()
#         return

#     # Fetch match details
#     match_details = get_match_details(selected_bet["match_id"])
#     if not match_details:
#         st.warning("Unable to fetch match details.")
#         st.button("Go Back", on_click=lambda: st.session_state.update({"current_page": "show_bets"}))
#         st.rerun()
#         return

#     # Add match details to the selected bet
#     selected_bet["home_team"] = match_details["home_team"]
#     selected_bet["away_team"] = match_details["away_team"]

#     # Display the bet details
#     st.markdown(
#         f"""
#         <div style='border: 2px solid #4CAF50; border-radius: 10px; padding: 15px; margin: 20px; background-color: #f9f9f9;'>
#             <h3 style='color: #4CAF50;'>Match: {selected_bet['home_team']} vs {selected_bet['away_team']}</h3>
#             <p><b>Selected Team:</b> {selected_bet['selected_team']}</p>
#             <p><b>Bet Type:</b> {selected_bet['bet_type']}</p>
#             <p><b>Amount:</b> {selected_bet['amount']} </p>
#             <p><b>Potential Win:</b> {selected_bet['potential_win']} </p>
#             <p><b>Created At:</b> {selected_bet['created_at']}</p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     # Form for user input
#     st.subheader("Edit Your Bet")

#     # Select the bet type (win/lose/draw)
#     selected_bet["bet_type"] = st.radio(
#         "Select Bet Type",
#         options=["win", "lose", "draw"],
#         index=["win", "lose", "draw"].index(selected_bet["bet_type"])
#     )

#     # Select the team
#     selected_bet["selected_team"] = st.selectbox(
#         "Select Team",
#         [selected_bet["home_team"], selected_bet["away_team"]],
#         index=0 if selected_bet["selected_team"] == selected_bet["home_team"] else 1
#     )

#     # Input amount
#     selected_bet["amount"] = st.number_input("Amount", min_value=0.0, value=float(selected_bet["amount"]), step=1.0)

#     # Calculate potential win
#     selected_bet["potential_win"] = round(selected_bet["amount"] * selected_bet["coefficient"], 2)
#     st.write(f"Potential Win: {selected_bet['potential_win']}")

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         if st.button("Confirm"):
#             update_bet_status(selected_bet["bet_id"], "pending")
#             st.session_state["current_page"] = "show_bets"
#             st.rerun()

#     with col2:
#         if st.button("Cancel"):
#             update_bet_status(selected_bet["bet_id"], "waiting_list")
#             st.session_state["current_page"] = "show_bets"
#             st.rerun()

#     with col3:
#         if st.button("Back"):
#             st.session_state["current_page"] = "show_bets"
#             st.rerun()
