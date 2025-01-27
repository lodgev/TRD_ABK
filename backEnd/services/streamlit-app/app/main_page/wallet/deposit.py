import streamlit as st
import requests

API_BASE_URL_DEPOSIT = "http://deposit-service:80"
API_BASE_URL_USAGE = "http://usage-service:80"


def deposit_funds():
    st.subheader("Deposit Funds")
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("Please log in to access your wallet.")
        return

    response_wallet = requests.get(f"{API_BASE_URL_USAGE}/wallet/user/{st.session_state.user_id}")

    if response_wallet.status_code == 200:
        wallet_id = response_wallet.json().get("id")
        amount = st.number_input("Enter Deposit Amount:", min_value=10, step=1)



        if st.button("Deposit"):
            payload = {"wallet_id": wallet_id, "amount": amount}
            response = requests.post(f"{API_BASE_URL_DEPOSIT}/deposit/", json=payload)

            if response.status_code == 200:
                st.success(f"Successfully deposited {amount} to wallet ID {wallet_id}.")
            else:
                st.error(f"Error depositing funds: {response.json().get('detail', 'Unknown error')}")

    else:
        st.error(f"Error fetching wallet ID: {response_wallet.json().get('detail', 'Unknown error')}")

