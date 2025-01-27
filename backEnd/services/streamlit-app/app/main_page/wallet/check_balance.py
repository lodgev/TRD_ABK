import streamlit as st
import requests
from datetime import datetime

API_BASE_URL_USAGE = "http://usage-service:80"
API_BASE_URL_DEPOSIT = "http://deposit-service:80"
API_BASE_URL_WITHDRAWAL = "http://withdrawal-service:80"

def format_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except ValueError:
        return date_str

def check_balance():
    st.divider()
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("Please log in to access your wallet.")
        return

    response_wallet = requests.get(f"{API_BASE_URL_USAGE}/wallet/user/{st.session_state.user_id}")

    if response_wallet.status_code == 200:
        wallet_id = response_wallet.json().get("id")

        # Получение баланса кошелька
        response_balance = requests.get(f"{API_BASE_URL_USAGE}/wallet/{wallet_id}/balance")

        if response_balance.status_code == 200:
            data = response_balance.json()

            st.markdown(
                f"<h2 style='text-align: center; font-size: 36px; font-weight: bold;'>Balance: {data['balance']} {data['currency']}</h2>",
                unsafe_allow_html=True
            )

            response_deposits = requests.get(f"{API_BASE_URL_DEPOSIT}/deposit/{wallet_id}")
            if response_deposits.status_code == 200:
                deposits = response_deposits.json()
                deposit_list = [
                    f"<b>Amount:</b> {d['amount']}<br><b>Date:</b> {format_date(d['created_at'])}"
                    for d in deposits
                ]
            else:
                deposit_list = ["No deposits found."]

            response_withdrawals = requests.get(f"{API_BASE_URL_WITHDRAWAL}/withdrawal/{wallet_id}")
            if response_withdrawals.status_code == 200:
                withdrawals = response_withdrawals.json()
                withdrawal_list = [
                    f"<b>Amount:</b> {w['amount']}<br><b>Date:</b> {format_date(w['created_at'])}"
                    for w in withdrawals
                ]
            else:
                withdrawal_list = ["No withdrawals found."]

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Deposit History")
                for deposit in deposit_list:
                    st.markdown(
                        f"""
                        <div style='
                            border: 1px solid #ddd;
                            padding: 15px;
                            border-radius: 10px;
                            margin-bottom: 10px;
                            background-color: #f9f9f9;
                            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                            '>
                            {deposit}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with col2:
                st.subheader("Withdrawal History")
                for withdrawal in withdrawal_list:
                    st.markdown(
                        f"""
                        <div style='
                            border: 1px solid #ddd;
                            padding: 15px;
                            border-radius: 10px;
                            margin-bottom: 10px;
                            background-color: #f9f9f9;
                            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                            '>
                            {withdrawal}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:
            st.error(f"Error fetching balance: {response_balance.json().get('detail', 'Unknown error')}")
    else:
        st.error(f"Error fetching wallet ID: {response_wallet.json().get('detail', 'Unknown error')}")
