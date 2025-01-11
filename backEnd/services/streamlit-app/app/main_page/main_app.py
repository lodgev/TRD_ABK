import streamlit as st
# from .matches import show_matches
# from .profile import show_profile
# from .betting import show_betting

def run_main_app():
    st.title("Main Application")
    main_mode = st.sidebar.selectbox("Select an option", ["Matches", "Profile", "Betting"])

    if main_mode == "Matches":
        st.write("In progress..")
    elif main_mode == "Profile":
        st.write("In progress..")
    elif main_mode == "Betting":
        st.write("In progress..")
