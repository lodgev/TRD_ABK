# import streamlit as st
# import requests
# import pandas as pd

# API_BASE_URL = "http://match-service:80/matches"

# def fetch_matches():
#     try:
#         response = requests.get(API_BASE_URL)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.error(f"Failed to fetch matches: {response.status_code}")
#             return []
#     except Exception as e:
#         st.error(f"An error occurred while fetching matches: {e}")
#         return []

# def show_matches():
#     st.title("Matches")

#     matches = fetch_matches()
#     if not matches:
#         st.info("No matches available.")
#         return

#     df = pd.DataFrame(matches)

#     st.sidebar.header("Filters")


#     teams = pd.concat([df["home_team"], df["away_team"]]).unique()
#     selected_team = st.sidebar.multiselect("Filter by team", teams)

#     if selected_team:
#         df = df[(df["home_team"].isin(selected_team)) | (df["away_team"].isin(selected_team))]

#     st.sidebar.header("Sorting")
#     sort_by = st.sidebar.selectbox("Sort by", ["match_date"])
#     sort_order = st.sidebar.radio("Sort order", ["Ascending", "Descending"])
#     ascending = sort_order == "Ascending"

#     df = df.sort_values(by=sort_by, ascending=ascending)

#     for _, row in df.iterrows():
#         with st.container():
#             st.markdown(
#                 f"""
#                 <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
#                     <h3>{row["home_team"]} vs {row["away_team"]}</h3>
#                     <p><b>Date:</b> {row["match_date"]}</p>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
import streamlit as st
import requests
import pandas as pd
import datetime

API_BASE_URL = "http://match-service:80/matches"

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
    st.title("Matches")

    matches = fetch_matches()
    if not matches:
        st.info("No matches available.")
        return

    df = pd.DataFrame(matches)

    df["match_date"] = pd.to_datetime(df["match_date"]).dt.strftime('%Y-%m-%d %H:%M:%S')

    st.sidebar.header("Filters")



    default_start_date = datetime.date(2024, 9, 17)


    start_date = st.sidebar.date_input("Start Date", value=default_start_date)
    end_date = st.sidebar.date_input("End Date", value=default_start_date + datetime.timedelta(days=1))

    if start_date and end_date:
        filtered_dates = (df["match_date"] >= start_date.strftime('%Y-%m-%d')) & (df["match_date"] <= end_date.strftime('%Y-%m-%d'))
        df = df[filtered_dates]


    teams = pd.concat([df["home_team"], df["away_team"]]).unique()
    selected_team = st.sidebar.multiselect("Filter by team", teams)
    if selected_team:
        df = df[(df["home_team"].isin(selected_team)) | (df["away_team"].isin(selected_team))]

    st.sidebar.header("Sorting")
    sort_by = st.sidebar.selectbox("Sort by", ["match_date"])
    sort_order = st.sidebar.radio("Sort order", ["Ascending", "Descending"])
    ascending = sort_order == "Ascending"

    df = df.sort_values(by=sort_by, ascending=ascending)

    for _, row in df.iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px;'>
                    <h3>{row["home_team"]} vs {row["away_team"]}</h3>
                    <p><b>Date:</b> {row["match_date"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
