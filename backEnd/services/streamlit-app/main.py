import streamlit as st
from app.auth_form.main_auth import run_auth
from app.main_page.main_app import run_main_app


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


if not st.session_state.authenticated:
    run_auth()
else:
    run_main_app()
