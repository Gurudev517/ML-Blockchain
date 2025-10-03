from flask import Flask, render_template, request
import numpy as np
import pickle
import os
from web3 import Web3

app = Flask(__name__, template_folder="templates")

# ----------------------
# Load models
# ----------------------
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

models = {}
for name in ["logistic_model", "decision_tree_model", "random_forest_model", "svm_model"]:
    with open(os.path.join(MODEL_DIR, f"{name}.pkl"), "rb") as f:
        models[name] = pickle.load(f)

# Load accuracies
with open(os.path.join(MODEL_DIR, "accuracies.pkl"), "rb") as f:
    accuracies = pickle.load(f)

# ----------------------
# Web3 Setup
# ----------------------
INFURA_URL = "https://sepolia.infura.io/v3/591a5c339ebd449ba8bd5a767290d5cb"
PRIVATE_KEY = "d1e6f833fcb720bc7428d8cf1d479641bfedbb75b08efbddd7c70f43cf3bad30"  # Replace with your private key
ACCOUNT_ADDRESS = "0x578EBf0501c9c108AD61B1dEcc90242907c5BD70"  # Replace with your wallet address

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
print("Web3 connected:", web3.is_connected())

CONTRACT_ADDRESS = "0xb52A6723904452769c7d368A519486e46547a0Fe"
CONTRACT_ABI = [ 
    { "anonymous": False, "inputs": [ { "indexed": False, "internalType": "uint256", "name": "loanId", "type": "uint256" }, { "indexed": False, "internalType": "address", "name": "borrower", "type": "address" }, { "indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256" }, { "indexed": False, "internalType": "uint256", "name": "duration", "type": "uint256" }, { "indexed": False, "internalType": "string", "name": "decision", "type": "string" } ], "name": "LoanStored", "type": "event" },
    { "inputs": [ { "internalType": "uint256", "name": "_loanId", "type": "uint256" } ], "name": "getLoan", "outputs": [ { "internalType": "address", "name": "borrower", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "uint256", "name": "duration", "type": "uint256" }, { "internalType": "string", "name": "decision", "type": "string" } ], "stateMutability": "view", "type": "function" },
    { "inputs": [], "name": "loanCount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" },
    { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "loans", "outputs": [ { "internalType": "address", "name": "borrower", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "uint256", "name": "duration", "type": "uint256" }, { "internalType": "string", "name": "decision", "type": "string" } ], "stateMutability": "view", "type": "function" },
    { "inputs": [ { "internalType": "uint256", "name": "_amount", "type": "uint256" }, { "internalType": "uint256", "name": "_duration", "type": "uint256" }, { "internalType": "string", "name": "_decision", "type": "string" } ], "name": "storeLoan", "outputs": [], "stateMutability": "nonpayable", "type": "function" }
]

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# ----------------------
# Routes
# ----------------------
@app.route("/")
def index():
    return render_template("loanform.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect form data
        annual_income = float(request.form["Annual Income"])
        loan_amount = float(request.form["Loan Amount"])
        employment_status = request.form["Employment Status"]
        total_assets = float(request.form["Total Assets"])
        home_ownership = request.form["Home Ownership"]
        credit_score = float(request.form["Credit Score"])

        # Add a loan duration (for blockchain demo)
        loan_duration = 12  # fixed 12 months for now

        # Encode categorical variables
        emp_map = {"Employed": 0, "Self-employed": 1, "Unemployed": 2, "Student": 3}
        home_map = {"Own": 0, "Rent": 1, "Mortgage": 2}

        employment_status = emp_map.get(employment_status, 0)
        home_ownership = home_map.get(home_ownership, 0)

        # Prepare input
        features = np.array([
            annual_income, loan_amount, employment_status,
            total_assets, home_ownership, credit_score
        ]).reshape(1, -1)

        # Predictions
        results = {}
        for name, model in models.items():
            pred = model.predict(features)[0]
            results[name] = {
                "prediction": "✅ Approved" if pred == 1 else "❌ Rejected",
                "accuracy": round(accuracies[name] * 100, 2)
            }

        # Best model (highest accuracy)
        best_model = max(results, key=lambda x: results[x]["accuracy"])
        final_prediction = results[best_model]["prediction"]

        # ---------------- Blockchain Part ----------------
        decision = "Approved" if "Approved" in final_prediction else "Rejected"

        nonce = web3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        txn = contract.functions.storeLoan(int(loan_amount), loan_duration, decision).build_transaction({
            "from": ACCOUNT_ADDRESS,
            "nonce": nonce,
            "gas": 300000,
            "gasPrice": web3.to_wei("10", "gwei")
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_hash_hex = web3.to_hex(tx_hash)

        # Render result page with loan info
        return render_template(
            "result.html",
            predictions=results,
            final=final_prediction,
            tx_hash=tx_hash_hex,
            loan_amount=loan_amount,
            loan_duration=loan_duration
        )

    except Exception as e:
        return f"<h3>Error: {e}</h3>"

if __name__ == "__main__":
    app.run(debug=True)


