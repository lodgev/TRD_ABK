import streamlit as st
import requests

API_BASE_URL_WITHDRAWAL = "http://withdrawal-service:80"
API_BASE_URL_USAGE = "http://usage-service:80"

def withdraw_funds():
    st.divider()
    st.subheader("Withdraw Funds")

    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("Please log in to access your wallet.")
        return

    response_wallet = requests.get(f"{API_BASE_URL_USAGE}/wallet/user/{st.session_state.user_id}")

    if response_wallet.status_code == 200:
        wallet_id = response_wallet.json().get("id")
        amount = st.number_input("Enter Withdrawal Amount:", min_value=10, step=1)

        if st.button("Withdraw"):
            payload = {"wallet_id": wallet_id, "amount": amount}
            response = requests.post(f"{API_BASE_URL_WITHDRAWAL}/withdrawal/", json=payload)

            if response.status_code == 200:
                st.success(f"Successfully withdrew {amount} from wallet ID {wallet_id}.")
            else:
                st.error(f"Error withdrawing funds: {response.json().get('detail', 'Unknown error')}")

    else:
        st.error(f"Error fetching wallet ID: {response_wallet.json().get('detail', 'Unknown error')}")

