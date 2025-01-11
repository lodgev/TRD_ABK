import streamlit as st
import requests


def show_login():
    
    st.markdown("<h2 style='text-align: center;'>Login</h2>", unsafe_allow_html=True)

    with st.form(key="login_form"):
        email = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        login_button = st.form_submit_button("Login")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Registration"):
            st.warning("In progress")
    with col2:
        if st.button("Forget password"):
            st.warning("In progress")

    if login_button:
        if email and password:
            #POST запит до auth-service
            try:
                print("trying")
                response = requests.post(
                    "http://auth-service:80/auth/login",
                    json={"email": email, "password": password},
                )

                if response.status_code == 200:
                    st.success("Login successful!")
                    st.session_state.authenticated = True  
                    st.rerun()  
                else:
                    st.error("Invalid email or password.")
            except requests.exceptions.RequestException:
                st.error("500 Internal Server Error. Could not connect to the authorization service")
        else:
            st.error("Please fill in all fields.")

