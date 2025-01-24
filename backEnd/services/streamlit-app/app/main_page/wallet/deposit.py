import streamlit as st
import requests

API_BASE_URL = "http://deposit-service:80"


def deposit_funds():
    st.subheader("Deposit Funds")

    wallet_id = st.number_input("Enter Wallet ID:", min_value=1, step=1)
    amount = st.number_input("Enter Deposit Amount:", min_value=0.01, step=0.01)

    if st.button("Deposit"):
        payload = {"wallet_id": wallet_id, "amount": amount}
        response = requests.post(f"{API_BASE_URL}/deposits/", json=payload)

        if response.status_code == 200:
            st.success(f"Successfully deposited {amount} to wallet ID {wallet_id}.")
        else:
            st.error(f"Error depositing funds: {response.json().get('detail', 'Unknown error')}")
