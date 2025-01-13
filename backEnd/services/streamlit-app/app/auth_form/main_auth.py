import streamlit as st
from .login import show_login
from .register import show_registration
from .forgot_password import show_forgot_password
from .reset_password import show_reset_password

def run_auth():

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Login"


    if st.session_state.current_page == "Login":
        show_login()
    elif st.session_state.current_page == "Register":
        show_registration()
    elif st.session_state.current_page == "Forgot password":
        show_forgot_password()
    elif st.session_state.current_page == "Reset password":
        show_reset_password()
        
