import streamlit as st
from app.main_page.bets.show_bets import show_bets
from app.main_page.bets.place_bet import place_bet_page

def run_main_bet():
    
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "show_bets" 

    st.write(f"Current Page: {st.session_state['current_page']}")

    if st.session_state.get("rerun_flag"):
        st.session_state.rerun_flag = False
        st.rerun()

    if st.session_state["current_page"] == "place_bet":
        place_bet_page()
    elif st.session_state["current_page"] == "show_bets":
        show_bets()
    else:
        st.error("Unexpected page encountered.")
        st.session_state["current_page"] = "show_bets" 
        st.rerun()

