import streamlit as st
import requests

def logout_user():
    access_token = st.session_state.get("access_token")
    user_id = st.session_state.get("user_id")

    if not access_token or not user_id:
        st.error("Missing authentication details.")
        return

    try:
        response = requests.post(
            "http://auth-service:80/auth/logout",
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
            json={"id": user_id}  
        )

        if response.status_code == 200:
            st.success("Successfully logged out!")
        
            st.session_state.authenticated = False
            st.session_state.access_token = None
            st.session_state.user_id = None
            st.session_state.rerun_flag = True
            # st.rerun()  
        else:
            st.error(f"Failed to log out. {response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.RequestException:
        st.error("Could not connect to the logout service.")
