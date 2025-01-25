

import streamlit as st
import requests
import pandas as pd

API_CLUBS_BASE_URL = "http://match-service:80/clubs"
API_RECOMMENDER_BASE_URL = "http://recommender-service:80/actions"



def record_user_action(club_id, action):

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("You need to log in to perform this action.")
        return

    try:
        payload = {
            "club_id": club_id,
            "user_id": user_id,
            "action": action,  # "liked" or "disliked"
        }
        response = requests.post(API_RECOMMENDER_BASE_URL, json=payload)
        if response.status_code == 200:
            st.success(f"Action '{action}' recorded for club ID {club_id}.")
        else:
            st.error(f"Failed to record user action: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred while recording user action: {e}")


def update_club_likes(club_id, action):
    try:
        payload = {"action": action}  # "like" or "dislike"
        response = requests.post(f"{API_CLUBS_BASE_URL}/{club_id}/update-likes", json=payload)
        if response.status_code == 200:
            st.success(f"Club {club_id} updated successfully!")
        else:
            st.error(f"Failed to update club likes/dislikes: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred while updating club likes/dislikes: {e}")


def fetch_clubs():
    """Fetch all clubs from the clubs API."""
    try:
        response = requests.get(API_CLUBS_BASE_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch clubs: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching clubs: {e}")
        return []


def show_clubs():
    st.title("Clubs")

    # Fetch clubs data
    clubs = fetch_clubs()
    if not clubs:
        st.info("No clubs available.")
        return

    # Convert clubs data to a DataFrame
    df = pd.DataFrame(clubs)

    # ==== Search Bar ====
    search_query = st.text_input("Search by club name or country")
    if search_query:
        df = df[df["club"].str.contains(search_query, case=False, na=False) | df["country"].str.contains(search_query, case=False, na=False)]

    # ==== Filters ====
    st.sidebar.header("Filters")
    selected_club = st.sidebar.multiselect("Filter by club", df["club"].unique())
    selected_level = st.sidebar.multiselect("Filter by level", df["level"].unique())
    selected_country = st.sidebar.multiselect("Filter by country", df["country"].unique())

    if selected_club:
        df = df[df["club"].isin(selected_club)]
    if selected_level:
        df = df[df["level"].isin(selected_level)]
    if selected_country:
        df = df[df["country"].isin(selected_country)]

    # ==== Sorting ====
    st.sidebar.header("Sorting")
    sort_by = st.sidebar.selectbox("Sort by", ["level", "elo", "start_date"])
    sort_order = st.sidebar.radio("Sort order", ["Ascending", "Descending"])
    ascending = sort_order == "Ascending"

    df = df.sort_values(by=sort_by, ascending=ascending)

    # ==== Display Clubs ====
    for _, row in df.iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
                    <h3>{row["club"]}</h3>
                    <p><b>Rank:</b> {row["rank"]}</p>
                    <p><b>Country:</b> {row["country"]}</p>
                    <p><b>Level:</b> {row["level"]}</p>
                    <p><b>Elo:</b> {row["elo"]}</p>
                    <p><b>Start Date:</b> {row["start_date"]}</p>
                    <p><b>End Date:</b> {row["end_date"]}</p>
                    <p><b>Likes:</b> {row["likes"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Like {row['club']}", key=f"like_{row['id']}"):
                    record_user_action(row["id"], "liked")
                    update_club_likes(row["id"], "like")
                    st.rerun()
            with col2:
                if st.button(f"Dislike {row['club']}", key=f"dislike_{row['id']}"):
                    record_user_action(row["id"], "disliked")
                    update_club_likes(row["id"], "dislike")
                    st.rerun()
