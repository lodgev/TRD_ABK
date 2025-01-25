import streamlit as st
from app.auth_form.logout import logout_user
from app.main_page.matches.show_clubs import show_clubs
from app.main_page.matches.show_matches import show_matches
from app.main_page.bets.bet_main import run_main_bet
from app.main_page.wallet.wallet_main import run_wallet_section


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

    st.title("TRD - The Real Deal")


    main_mode = st.sidebar.selectbox("Select an option", ["Matches", "Clubs", "Profile", "Betting", "Wallet"])

    if main_mode == "Matches":
        show_matches()
    elif main_mode == "Clubs":
        show_clubs() 
    elif main_mode == "Profile":
        st.write("Profile section is in progress...")
    elif main_mode == "Betting":
        run_main_bet()
    elif main_mode == "Wallet":
        run_wallet_section()

