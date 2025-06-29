import streamlit as st
import requests
import jwt


def show_login():
    st.markdown("<h2 style='text-align: center;'>Login</h2>", unsafe_allow_html=True)

    with st.form(key="login_form"):
        email = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        login_button = st.form_submit_button("Login")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Registration"):
            st.session_state.current_page = "Register"
            st.rerun()
    with col2:
        if st.button("Forgot password"):
            st.session_state.current_page = "Forgot password"
            st.rerun()

    if login_button:
        if email and password:
            try:
                response = requests.post(
                    "http://auth-service:80/auth/login",
                    json={"email": email, "password": password},
                )

                if response.status_code == 200:
                    st.success("Login successful!")

                    data = response.json()
                    st.session_state.authenticated = True
                    st.session_state.access_token = data.get("access_token")
                    st.session_state.user_id = jwt.decode(
                        data.get("access_token"),
                        "ed73c27f0152572f885e87d1435153c56865d7ee379ffa0c89c6242616effade",
                        algorithms=["HS256"]
                    ).get("user_id")
                    st.rerun()
                elif response.status_code == 403:
                    st.error("Your email is not verified. Please check your email to verify your account.")
                elif response.status_code == 401:
                    st.error("Invalid email or password.")
                else:
                    st.error(f"Unexpected error occurred: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the authorization service: {e}")
        else:
            st.error("Please fill in all fields.")
