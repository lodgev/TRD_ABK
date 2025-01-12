# import streamlit as st
# import requests


# def show_registration():
#     st.title("Registration Form")

#     firstname = st.text_input("First Name", placeholder="Enter your first name")
#     lastname = st.text_input("Last Name", placeholder="Enter your last name")
#     email = st.text_input("Email", placeholder="Enter your email address")
#     password = st.text_input("Password", type="password", placeholder="Enter your password")
    
#     if st.button("Register"):
#         if not firstname or not lastname or not email or not password:
#             st.error("Please fill in all fields.")
#             return

#         try:
#             response = requests.post(
#                 "http://auth-service:80/auth/register",
#                 json={
#                     "firstname": firstname,
#                     "lastname": lastname,
#                     "email": email,
#                     "password": password,
#                 },
#                 headers={"Content-Type": "application/json"}
#             )

#             if response.status_code == 200:
#                 st.success("Registration successful!")
#             elif response.status_code == 400:
#                 st.error("A user with this email already exists.")
#             else:
#                 st.error("An error occurred. Please try again later.")
#         except requests.exceptions.RequestException as e:
#             st.error(f"Failed to connect to the registration service: {e}")

#     if st.button("Back to Login"):
#         st.session_state.current_page = "Login"
#         st.rerun()
import streamlit as st
import requests


def show_registration():
    st.title("Registration Form")

    firstname = st.text_input("First Name", placeholder="Enter your first name")
    lastname = st.text_input("Last Name", placeholder="Enter your last name")
    email = st.text_input("Email", placeholder="Enter your email address")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Register"):
        if not firstname or not lastname or not email or not password:
            st.error("Please fill in all fields.")
            return

        try:
            response = requests.post(
                "http://auth-service:80/auth/register",
                json={
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email,
                    "password": password,
                },
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                st.success("Registration successful! A verification email has been sent.")
            elif response.status_code == 400:
                st.error("A user with this email already exists.")
            elif response.status_code == 500:
                st.error("Failed to send verification email. Please try again later.")
            else:
                st.error(f"Unexpected error occurred: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the registration service: {e}")

    if st.button("Back to Login"):
        st.session_state.current_page = "Login"
        st. rerun()
