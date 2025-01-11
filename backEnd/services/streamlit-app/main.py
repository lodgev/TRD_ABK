import streamlit as st
from app.auth_form.login import show_login
from app.main_page.main_app import run_main_app


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


if not st.session_state.authenticated:
    show_login()
else:
    run_main_app()
