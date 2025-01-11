import streamlit as st
from .login import show_login
# from .register import show_register
# from .reset_password import show_reset_password

def run_auth():
    st.title("Authentication")
    auth_mode = st.sidebar.selectbox("Select an option", ["Login", "Register", "Reset Password"])

    if auth_mode == "Login":
        show_login()
    elif auth_mode == "Register":
        st.write("In progress..")
        # show_register()
    elif auth_mode == "Reset Password":
        st.write("In progress..")
