import streamlit as st
import requests

API_BASE_URL = "http://withdrawal-service:80"


def withdraw_funds():
    st.subheader("Withdraw Funds")
    # todo : fetch wallet id automatically
    wallet_id = st.number_input("Enter Wallet ID:", min_value=1, step=1)
    amount = st.number_input("Enter Withdrawal Amount:", min_value=0.01, step=0.01)

    if st.button("Withdraw"):
        payload = {"wallet_id": wallet_id, "amount": amount}
        response = requests.post(f"{API_BASE_URL}/withdrawal/", json=payload)

        if response.status_code == 200:
            st.success(f"Successfully withdrew {amount} from wallet ID {wallet_id}.")
        else:
            st.error(f"Error withdrawing funds: {response.json().get('detail', 'Unknown error')}")
