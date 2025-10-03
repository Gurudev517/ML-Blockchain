from flask import Flask, render_template, request
import joblib
import numpy as np
from web3 import Web3
import os

app = Flask(__name__)

# --------------------------
# 1️⃣ Load ML Model
# --------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'loan_model.pkl')
model = joblib.load(MODEL_PATH)

# --------------------------
# 2️⃣ Blockchain Connection
# --------------------------
# Make sure your .env or hardhat node has these values correctly
INFURA_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"
CONTRACT_ADDRESS = "YOUR_DEPLOYED_CONTRACT_ADDRESS"
PRIVATE_KEY = "YOUR_WALLET_PRIVATE_KEY"      # ⚠ keep this secret
PUBLIC_ADDRESS = "YOUR_WALLET_PUBLIC_ADDRESS"

# Optional connection
try:
    web3 = Web3(Web3.HTTPProvider(INFURA_URL))
    if web3.is_connected():
        print("✅ Connected to Sepolia Testnet")
    else:
        print("❌ Failed to connect to Sepolia")
except Exception as e:
    print(f"Blockchain connection error: {e}")
    web3 = None

# --------------------------
# 3️⃣ Routes
# --------------------------

@app.route('/')
def home():
    # Landing page (you can make a separate index.html for welcome screen)
    return render_template('loanform.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract form values
        gender = 1 if request.form['Gender'] == 'Male' else 0
        married = 1 if request.form['Married'] == 'Yes' else 0
        applicant_income = float(request.form['ApplicantIncome'])
        coapplicant_income = float(request.form['CoapplicantIncome'])
        loan_amount = float(request.form['LoanAmount'])
        credit_history = int(request.form['Credit_History'])

        # Prepare features in the order model expects
        features = np.array([[gender, married, applicant_income, coapplicant_income, loan_amount, credit_history]])
        prediction = model.predict(features)[0]

        result_text = "✅ Loan Approved" if prediction == 1 else "❌ Loan Rejected"

        # (Optional) store status on blockchain (if implemented in your contract)
        # You can trigger your contract method here if needed

        return render_template('result.html', result=result_text)

    except Exception as e:
        print(f"Prediction error: {e}")
        return "An error occurred during prediction. Check server logs."

@app.route('/check_status')
def check_status():
    # Here you could read data from the blockchain contract if required
    # For demo, we'll return a placeholder
    return "<h2 style='text-align:center;'>🔗 Blockchain status check will appear here.</h2>"

# --------------------------
# 4️⃣ Run the App
# --------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

