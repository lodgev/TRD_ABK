import streamlit as st
from app.auth_form.logout import logout_user
# from .matches import show_matches
# from .profile import show_profile
# from .betting import show_betting

def run_main_app():
    
    if st.session_state.get("rerun_flag"):
        st.session_state.rerun_flag = False
        st.rerun()
        
        
    st.markdown(
        """
        <style>
        .logout-button {
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.button(
            "Logout",
            key="logout",
            help="Log out of your account",
            on_click=logout_user,
        )

    st.title("Welcome to the Main Page!")
    st.write("Here is your main application content.")
    
    st.title("Main Application")
    main_mode = st.sidebar.selectbox("Select an option", ["Matches", "Profile", "Betting"])


    if main_mode == "Matches":
        st.write("In progress..")
    elif main_mode == "Profile":
        st.write("In progress..")
    elif main_mode == "Betting":
        st.write("In progress..")
