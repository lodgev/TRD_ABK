import streamlit as st
from .login import show_login
from .register import show_registration

def run_auth():

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Login"


    if st.session_state.current_page == "Login":
        show_login()
    elif st.session_state.current_page == "Register":
        show_registration()
    elif st.session_state.current_page == "Reset Password":
        st.write("Reset Password page is in progress...") 
