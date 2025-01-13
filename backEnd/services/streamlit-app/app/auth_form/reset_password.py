import streamlit as st
import requests

def show_reset_password():
    st.title("Reset password")

    reset_token = st.text_input("Reset code", placeholder="Enter the 6-digit code from your email")
    new_password = st.text_input("New Password", type="password", placeholder="Enter your new password")

    if st.button("Reset Password"):
        if not reset_token or not new_password:
            st.error("Please fill in all fields.")
            return

        try:
            response = requests.post(
                f"http://auth-service:80/auth/reset-password",
                json={"reset_token": reset_token, "new_password": new_password},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                st.success("Password reset successfully! You can now log in with your new password.")
                st.session_state.current_page = "Login"
                st.rerun()
            else:
                st.error(response.json().get("detail", "An error occurred."))
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the reset password service: {e}")
