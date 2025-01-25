import streamlit as st
import requests

API_BASE_URL = "http://usage-service:80"

def check_balance():
    st.subheader("Check Wallet Balance")

    wallet_id = st.number_input("Enter Wallet ID:", min_value=1, step=1)

    if st.button("Check Balance"):
        response = requests.get(f"{API_BASE_URL}/wallets/{wallet_id}/balance")

        if response.status_code == 200:
            data = response.json()
            st.write(f"**Balance:** {data['balance']}") #{data['currency']}
        else:
            st.error(f"Error fetching balance: {response.json().get('detail', 'Unknown error')}")
