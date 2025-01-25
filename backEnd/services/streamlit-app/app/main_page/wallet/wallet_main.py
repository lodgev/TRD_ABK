import streamlit as st
from app.main_page.wallet.deposit import deposit_funds
from app.main_page.wallet.withdraw import withdraw_funds
from app.main_page.wallet.check_balance import check_balance
# TODO: сделать нормально
def run_wallet_section():
    st.title("💰 Wallet Management")

    action = st.sidebar.radio("Choose an action", ["Check Balance", "Deposit Funds", "Withdraw Funds"])

    if action == "Check Balance":
        check_balance()
    elif action == "Deposit Funds":
        deposit_funds()
    elif action == "Withdraw Funds":
        withdraw_funds()
