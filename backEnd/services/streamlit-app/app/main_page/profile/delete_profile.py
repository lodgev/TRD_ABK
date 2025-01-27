import streamlit as st
import requests

API_BASE_URL = "http://usermanagement-service:6666/UserManagementService/users"

def delete_profile():
    st.subheader("Delete Account")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("You need to be logged in to delete your account.")
        return

    st.warning("Deleting your account is permanent and cannot be undone.")
    confirm = st.checkbox("I understand the consequences and wish to proceed.")

    if confirm and st.button("Delete Account"):
        try:
            response = requests.delete(f"{API_BASE_URL}/{user_id}")
            if response.status_code == 200:
                st.success("Your account has been deleted successfully.")
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.experimental_rerun()
            else:
                st.error(f"Failed to delete account: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
