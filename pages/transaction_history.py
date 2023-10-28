import streamlit as st
import pandas as pd
from bank import transaction_history

# Transaction History Page
st.header("Transaction History")
st.dataframe(transaction_history)

# # Save the transaction history to a CSV file (optional)
# transaction_history.to_csv("piggy_bank_transactions.csv", index=False)
