import streamlit as st
import pandas as pd
import os
import datetime

st.set_page_config(
    page_title="Piggy Bank",
    page_icon="🐷",
    layout='wide'
)

page_bg_img = '''
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://www.canva.com/design/DAFyNV1BemA/A8GBnWWBVhDJUB5y7MtZmw/view?utm_content=DAFyNV1BemA&utm_campaign=designshare&utm_medium=link&utm_source=editor");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load existing transaction history from a CSV file
transaction_history = pd.read_csv("piggy_bank_transactions.csv") if "piggy_bank_transactions.csv" in os.listdir(
) else pd.DataFrame(columns=["Type", "Date", "Amount", "Label/Reason", "Category"])
balance = transaction_history['Amount'].sum()

st.title("Welcome to Piggy Bank")

col1, col2 = st.columns(2)

# # Create a dataframe to store transaction history
# transaction_history = pd.DataFrame(
#     columns=["Type", "Date", "Amount", "Label/Reason"])

balance = 0

with col2:
   # Deposit Form
    st.header("Deposit Money")
    deposit_date = st.date_input(
        "Deposit Date", datetime.date.today())  # Unique key
    # Use float for min_value and step
    deposit_amount = st.number_input(
        "Deposit Amount", min_value=0.01, step=0.01)
    deposit_label = st.text_input("Label (optional)")  # Unique key
    if st.button("Deposit"):
        balance += deposit_amount  # Update the balance with the deposit amount
        #changed transaction_history.concat to transaction_history.append
        transaction_history = transaction_history.append({"Type": "Deposit", "Date": deposit_date,
                                                          "Amount": deposit_amount, "Label/Reason": deposit_label},
                                                         ignore_index=True)

    # Withdrawal Form
    st.header("Withdraw Money")
    withdraw_date = st.date_input(
        "Withdraw Date", datetime.date.today())  # Unique key
    # Use float for min_value and step
    withdraw_amount = st.number_input(
        "Withdraw Amount", min_value=0.01, step=0.01)
    withdraw_reason = st.text_input("Reason")  # Unique key
    withdraw_category = st.selectbox("Spent on", ["Select a category...", "Food", "Games", "Books", "Activity", "Other"])
    if st.button("Withdraw"):
        if withdraw_category == "Select a category...":
            st.warning("Please select a valid category.")
        else:
            if withdraw_amount <= balance:
                balance -= withdraw_amount  # Update the balance by subtracting the withdrawal amount
                 #changed transaction_history.concat to transaction_history.append
                transaction_history = transaction_history.append({"Type": "Withdrawal", "Date": withdraw_date,
                                                                "Amount": -withdraw_amount, "Label/Reason": withdraw_reason, 
                                                                "Category": withdraw_category},
                                                                ignore_index=True)
            else:
                st.warning("Withdrawal amount exceeds current balance.")

with col1:
    # Home page to display balance
    st.header("Piggy Bank Balance")
    st.write(f"Current Balance: ${balance:.2f}")

    # Save the transaction history to a CSV file (optional)
    transaction_history.to_csv("piggy_bank_transactions.csv", index=False)

    # New: Plotting a graph
    st.header("Spending Categories")
    withdrawals = transaction_history[transaction_history['Type'] == 'Withdrawal']
    spending_categories = withdrawals.groupby("Category")["Amount"].sum().abs().reset_index()
    st.bar_chart(spending_categories.rename(columns={"Amount": "Spending"}))