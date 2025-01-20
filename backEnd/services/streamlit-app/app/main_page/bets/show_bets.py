# import streamlit as st
# import requests
# import pandas as pd

# API_BASE_URL = "http://betting-service:80/betts"

# def fetch_bets(user_id):
#     try:
#         response = requests.get(f"{API_BASE_URL}/get-all-bets")
#         if response.status_code == 200:
#             bets = response.json()
#             # Filter bets based on the logged-in user
#             return [bet for bet in bets if bet["user_id"] == user_id]
#         else:
#             st.error(f"Failed to fetch bets: {response.status_code}")
#             return []
#     except Exception as e:
#         st.error(f"An error occurred while fetching bets: {e}")
#         return []

# def delete_bet(bet_id):
#     """Delete a bet."""
#     try:
#         response = requests.delete(f"{API_BASE_URL}/cancel-bet/{bet_id}")
#         if response.status_code == 200:
#             st.success(f"Bet ID {bet_id} deleted successfully!")
#         else:
#             st.error(f"Failed to delete bet: {response.status_code} - {response.json().get('detail', '')}")
#     except Exception as e:
#         st.error(f"An error occurred while deleting the bet: {e}")

# def show_bets():
#     st.title("My Bets")

#     # Assume the user_id is stored in session state after login
#     user_id = st.session_state.get("user_id")
#     if not user_id:
#         st.warning("You need to log in to view your bets.")
#         return

#     bets = fetch_bets(user_id)
#     if not bets:
#         st.info("No bets available.")
#         return

#     df = pd.DataFrame(bets)

#     tabs = st.tabs(["Betting Attent", "Betting In Course", "History"])

#     # **Betting Attent: status = waiting_list**
#     with tabs[0]:
#         st.header("Betting Attent")
#         attent_bets = df[df["status"] == "waiting_list"]
#         if attent_bets.empty:
#             st.write("No bets in the waiting list.")
#         else:
#             for _, row in attent_bets.iterrows():
#                 with st.container():
#                     st.markdown(
#                         f"""
#                         <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
#                             <h3>{row['selected_team']} ({row['bet_type']})</h3>
#                             <p><b>Match ID:</b> {row['match_id']}</p>
#                             <p><b>Amount:</b> {row['amount']}</p>
#                             <p><b>Potential Win:</b> {row['potential_win']}</p>
#                             <p><b>Status:</b> {row['status']}</p>
#                             <p><b>Created At:</b> {row['created_at']}</p>
#                         </div>
#                         """,
#                         unsafe_allow_html=True,
#                     )
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         if st.button(f"Place Bet (ID: {row['bet_id']})", key=f"place-{row['bet_id']}"):
#                             st.session_state["selected_bet"] = row.to_dict()
#                             st.session_state["current_page"] = "place_bet"
#                             st.rerun()
#                     with col2:
#                         if st.button(f"Remove (ID: {row['bet_id']})", key=f"remove-{row['bet_id']}"):
#                             delete_bet(row["bet_id"])
#                             st.rerun()

#     # **Betting In Course: status = pending**
#     with tabs[1]:
#         st.header("Betting In Course")
#         in_course_bets = df[df["status"] == "pending"]
#         if in_course_bets.empty:
#             st.write("No bets in course.")
#         else:
#             for _, row in in_course_bets.iterrows():
#                 with st.container():
#                     st.markdown(
#                         f"""
#                         <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
#                             <h3>{row['selected_team']} ({row['bet_type']})</h3>
#                             <p><b>Match ID:</b> {row['match_id']}</p>
#                             <p><b>Amount:</b> {row['amount']}</p>
#                             <p><b>Potential Win:</b> {row['potential_win']}</p>
#                             <p><b>Status:</b> {row['status']}</p>
#                             <p><b>Created At:</b> {row['created_at']}</p>
#                         </div>
#                         """,
#                         unsafe_allow_html=True,
#                     )
#                     if st.button(f"Cancel Bet (ID: {row['bet_id']})", key=f"cancel-{row['bet_id']}"):
#                         delete_bet(row["bet_id"])
#                         st.rerun()

#     # **History: status = won or lost**
#     with tabs[2]:
#         st.header("History")
#         history_bets = df[df["status"].isin(["won", "lost"])]
#         if history_bets.empty:
#             st.write("No betting history available.")
#         else:
#             for _, row in history_bets.iterrows():
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
import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "http://betting-service:80/betts"

def fetch_bets(user_id):
    """Fetch bets for the logged-in user."""
    try:
        response = requests.get(f"{API_BASE_URL}/get-all-bets")
        if response.status_code == 200:
            bets = response.json()
            # Filter bets based on the logged-in user
            return [bet for bet in bets if bet["user_id"] == user_id]
        else:
            st.error(f"Failed to fetch bets: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching bets: {e}")
        return []

def delete_bet(bet_id):
    """Delete a bet."""
    try:
        response = requests.delete(f"{API_BASE_URL}/cancel-bet/{bet_id}")
        if response.status_code == 200:
            st.success(f"Bet ID {bet_id} deleted successfully!")
        else:
            st.error(f"Failed to delete bet: {response.status_code} - {response.json().get('detail', '')}")
    except Exception as e:
        st.error(f"An error occurred while deleting the bet: {e}")

def show_bets():
    st.title("My Bets")

    # Assume the user_id is stored in session state after login
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("You need to log in to view your bets.")
        return

    bets = fetch_bets(user_id)
    if not bets:
        st.info("No bets available.")
        return

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
                    st.markdown(
                        f"""
                        <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
                            <h3>{row['selected_team']} ({row['bet_type']})</h3>
                            <p><b>Match ID:</b> {row['match_id']}</p>
                            <p><b>Amount:</b> {row['amount']}</p>
                            <p><b>Potential Win:</b> {row['potential_win']}</p>
                            <p><b>Status:</b> {row['status']}</p>
                            <p><b>Created At:</b> {row['created_at']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Place Bet (ID: {row['bet_id']})", key=f"place-{row['bet_id']}"):
                            # Save the selected bet to session state and navigate to place_bet page
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
                    st.markdown(
                        f"""
                        <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
                            <h3>{row['selected_team']} ({row['bet_type']})</h3>
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
                st.markdown(
                    f"""
                    <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
                        <h3>{row['selected_team']} ({row['bet_type']})</h3>
                        <p><b>Match ID:</b> {row['match_id']}</p>
                        <p><b>Amount:</b> {row['amount']}</p>
                        <p><b>Potential Win:</b> {row['potential_win']}</p>
                        <p><b>Status:</b> {row['status']}</p>
                        <p><b>Created At:</b> {row['created_at']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
