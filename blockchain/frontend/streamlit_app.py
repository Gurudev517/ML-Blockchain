import streamlit as st
import pickle
import numpy as np

# Load your trained ML model (example with pickle)
model = pickle.load(open("model.pkl", "rb"))

st.title("Loan Risk Prediction System")

# Input fields
age = st.number_input("Enter Age", min_value=18, max_value=100, step=1)
income = st.number_input("Enter Income", min_value=0)
loan_amount = st.number_input("Enter Loan Amount", min_value=0)

if st.button("Predict"):
    # Example: adjust features as per your model
    features = np.array([[age, income, loan_amount]])
    prediction = model.predict(features)
    
    if prediction[0] == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")
