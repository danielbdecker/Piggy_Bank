import streamlit as st
import pandas as pd
import os
import datetime

st.set_page_config(
    page_title="Piggy Bank",
    page_icon="🐷",
    layout='wide'
)

st.title("Welcome to Piggy Bank")

page_bg_img = '''
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://www.canva.com/design/DAFyNV1BemA/A8GBnWWBVhDJUB5y7MtZmw/view?utm_content=DAFyNV1BemA&utm_campaign=designshare&utm_medium=link&utm_source=editor");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


# Create a dataframe to store transaction history
transaction_history = pd.DataFrame(
    columns=["Type", "Date", "Amount", "Label/Reason"])
balance = 0

# Home page to display balance
st.header("Piggy Bank Balance")
st.write(f"Current Balance: ${balance:.2f}")

# Deposit Form
st.header("Deposit Money")
deposit_date = st.date_input(
    "Deposit Date", datetime.date.today())  # Unique key
# Use float for min_value and step
deposit_amount = st.number_input("Deposit Amount", min_value=0.01, step=0.01)
deposit_label = st.text_input("Label (optional)")  # Unique key
if st.button("Deposit"):
    balance += deposit_amount  # Update the balance with the deposit amount
    transaction_history = transaction_history.append({"Type": "Deposit", "Date": deposit_date,
                                                      "Amount": deposit_amount, "Label/Reason": deposit_label},
                                                     ignore_index=True)

# Withdrawal Form
st.header("Withdraw Money")
withdraw_date = st.date_input(
    "Withdraw Date", datetime.date.today())  # Unique key
# Use float for min_value and step
withdraw_amount = st.number_input("Withdraw Amount", min_value=0.01, step=0.01)
withdraw_reason = st.text_input("Reason")  # Unique key
if st.button("Withdraw"):
    if withdraw_amount <= balance:
        balance -= withdraw_amount  # Update the balance by subtracting the withdrawal amount
        transaction_history = transaction_history.append({"Type": "Withdrawal", "Date": withdraw_date,
                                                          "Amount": -withdraw_amount, "Label/Reason": withdraw_reason},
                                                         ignore_index=True)
    else:
        st.warning("Withdrawal amount exceeds current balance.")

# Transaction History Page
st.header("Transaction History")
st.dataframe(transaction_history)

# Save the transaction history to a CSV file (optional)
transaction_history.to_csv("piggy_bank_transactions.csv", index=False)
