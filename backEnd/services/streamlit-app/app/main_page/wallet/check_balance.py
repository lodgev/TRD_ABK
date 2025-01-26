import streamlit as st
import requests

API_BASE_URL = "http://usage-service:80"

# def check_balance():
#     st.subheader("Check Wallet Balance")
#     # todo : fetch wallet id automatically
#     wallet_id = st.number_input("Enter Wallet ID:", min_value=1, step=1)
#
#     if st.button("Check Balance"):
#         response = requests.get(f"{API_BASE_URL}/wallet/{wallet_id}/balance")
#
#         if response.status_code == 200:
#             data = response.json()
#             st.write(f"**Balance:** {data['balance']} {data['currency']}") #
#         else:
#             st.error(f"Error fetching balance: {response.json().get('detail', 'Unknown error')}")

def check_balance():
    st.subheader("Check Wallet Balance")

    # user_id = st.session_state.get("user_id")
    # if not user_id:
    #     st.warning("You need to log in to view your bets.")
    #     return
    #
    # bets = fetch_bets(user_id)
    # if not bets:
    #     st.info("No bets available.")
    #     return

    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("Please log in to access your wallet.")
        return

    # Получение ID кошелька по ID пользователя
    response_wallet = requests.get(f"{API_BASE_URL}/wallet/user/{st.session_state.user_id}")

    if response_wallet.status_code == 200:
        wallet_id = response_wallet.json().get("wallet_id")

        # Получение баланса по ID кошелька
        response_balance = requests.get(f"{API_BASE_URL}/wallet/{wallet_id}")

        if response_balance.status_code == 200:
            data = response_balance.json()
            st.write(f"**Balance:** {data['balance']} {data['currency']}")
        else:
            st.error(f"Error fetching balance: {response_balance.json().get('detail', 'Unknown error')}")
    else:
        st.error(f"Error fetching wallet ID: {response_wallet.json().get('detail', 'Unknown error')}")