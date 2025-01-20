import streamlit as st
from app.main_page.bets.show_bets import show_bets
from app.main_page.bets.place_bet import place_bet_page

def run_main_bet():
    # Ensure the current page is initialized to "show_bets"
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "show_bets" 

    # Debugging: Log current page
    st.write(f"Current Page: {st.session_state['current_page']}")

    # Handle rerun if necessary
    if st.session_state.get("rerun_flag"):
        st.session_state.rerun_flag = False
        st.rerun()

    # Navigate based on the current page
    if st.session_state["current_page"] == "place_bet":
        place_bet_page()
    elif st.session_state["current_page"] == "show_bets":
        show_bets()
    else:
        # Log unexpected state
        st.error("Unexpected page encountered.")
        st.session_state["current_page"] = "show_bets"  # Reset to default
        st.rerun()
