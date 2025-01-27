import streamlit as st
from app.main_page.profile.update_profile import update_profile
from app.main_page.profile.delete_profile import delete_profile

def run_profile_section():
    st.title("My Profile")

    st.sidebar.header("Profile Options")
    option = st.sidebar.radio(
        "Choose an action:",
        options=["Update Profile", "Delete Account"]
    )

    if option == "Update Profile":
        update_profile()
    elif option == "Delete Account":
        delete_profile()
