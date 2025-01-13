import streamlit as st
import requests

def show_forgot_password():
    st.title("Forgot Password")

    if "email_for_reset" not in st.session_state:
        email = st.text_input("Email", placeholder="Enter your email address")
        if st.button("Send reset code"):
            if not email:
                st.error("Please enter your email.")
                return

            try:
                response = requests.post(
                    "http://auth-service:80/auth/forgot-password",
                    json={"email": email},
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    st.success("A reset code has been sent to your email.")
                    st.session_state.email_for_reset = email 
                    st.session_state.current_page = "Reset password"
                    st.rerun()
                else:
                    st.error(response.json().get("detail", "An error occurred."))
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the reset password service: {e}")
        if st.button("Back to Login"):
            st.session_state.current_page = "Login"
            st.rerun()