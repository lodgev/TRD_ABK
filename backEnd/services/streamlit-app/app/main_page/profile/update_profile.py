import streamlit as st
import requests

API_BASE_URL = "http://usermanagement-service:6666/UserManagementService/users"

def update_profile():
    st.subheader("Update Profile")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("You need to be logged in to update your profile.")
        return

    # Fetch current profile details
    try:
        response = requests.get(f"{API_BASE_URL}/{user_id}")
        if response.status_code == 200:
            user_data = response.json()["user"]
        else:
            st.error(f"Failed to fetch user data: {response.status_code}")
            return
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return

    # Pre-fill fields with current data
    email = st.text_input("Email", value=user_data["email"])
    first_name = st.text_input("First Name", value=user_data["firstName"])
    last_name = st.text_input("Last Name", value=user_data["lastName"])

    if st.button("Update Profile"):
        updated_data = {
            "email": email,
            "firstName": first_name,
            "lastName": last_name
        }

        try:
            response = requests.put(f"{API_BASE_URL}/{user_id}", json=updated_data)
            if response.status_code == 200:
                st.success("Profile updated successfully!")
            else:
                st.error(f"Failed to update profile: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
