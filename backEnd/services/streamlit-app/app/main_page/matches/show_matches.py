import streamlit as st
import requests
import pandas as pd


API_BASE_URL = "http://match-service:80/clubs"


def fetch_matches():
    try:
        response = requests.get(API_BASE_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch matches: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching matches: {e}")
        return []


def show_matches():
    st.title("Clubs")


    matches = fetch_matches()
    if not matches:
        st.info("No matches available.")
        return

    df = pd.DataFrame(matches)

    search_query = st.text_input("Search by club name or country")
    if search_query:
        df = df[df["club"].str.contains(search_query, case=False, na=False) | df["country"].str.contains(search_query, case=False, na=False)]

    st.sidebar.header("Filters")
    selected_club = st.sidebar.multiselect("Filter by Club", df["club"].unique())
    selected_level = st.sidebar.multiselect("Filter by Level", df["level"].unique())
    selected_country = st.sidebar.multiselect("Filter by Country", df["country"].unique())

    if selected_club:
        df = df[df["club"].isin(selected_club)]
    if selected_level:
        df = df[df["level"].isin(selected_level)]
    if selected_country:
        df = df[df["country"].isin(selected_country)]

    st.sidebar.header("Sorting")
    sort_by = st.sidebar.selectbox("Sort by", ["level", "elo", "start_date"])
    sort_order = st.sidebar.radio("Sort order", ["Ascending", "Descending"])
    ascending = True if sort_order == "Ascending" else False

    df = df.sort_values(by=sort_by, ascending=ascending)

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
                </div>
                """,
                unsafe_allow_html=True,
            )

