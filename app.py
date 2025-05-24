import pandas as pd
import streamlit as st
import time
import random

# Load data once with caching
@st.cache_data
def load_data():
    xls = pd.ExcelFile('crap.xlsx')
    master_df = pd.read_excel(xls, sheet_name='Master_DB')
    di34_df = pd.read_excel(xls, sheet_name='DI34')
    master_df.columns = [col.strip() for col in master_df.columns]
    di34_df.columns = [col.strip() for col in di34_df.columns]
    return master_df, di34_df

def detect_fraud(comment):
    comment = comment.lower()
    keywords2 = ['deposit']
    if pd.isna(comment) or comment.strip() == "" or any(k in comment for k in keywords2):
        return "Suspicious"
    keywords = ['unauthorized', 'dispute', 'fraud', 'not recognized', 'lost', 'stolen', 'overdrawn', 'provisional credit']
    if any(k in comment for k in keywords):
        return "Fraudulent"
    return "Legit"

# UI
st.title("🕵️ Fraud Detection Dashboard")

if st.button("▶️ Run Rules"):
    with st.spinner("⏳ Running rules... Please wait..."):
        time.sleep(random.randint(5, 10))  # Delay of 5–10 seconds

        master_df, di34_df = load_data()
        merged_df = pd.merge(
            master_df,
            di34_df,
            left_on='SSN Number',
            right_on='SSN_Number',
            how='inner'
        )

        merged_df['Fraud_Flag'] = merged_df['Commets'].apply(detect_fraud)
        fraud_df = merged_df[merged_df['Fraud_Flag'].isin(['Fraudulent', 'Suspicious'])]

        st.success(f"🚨 Potential Fraudulent Transactions: {len(fraud_df)} found")
        st.dataframe(fraud_df[['SSN Number', 'DOB', 'Account_No', 'Transaction Amount', 'Commets', 'Fraud_Flag']])

        csv = fraud_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Fraud Records as CSV", csv, "fraudulent_transactions.csv", "text/csv")
else:
    st.info("Click the ▶️ **Run Rules** button to start fraud detection.")
