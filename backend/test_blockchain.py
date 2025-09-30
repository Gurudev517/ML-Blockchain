from web3 import Web3
import json

# ✅ Connect to Hardhat local blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
print("🔗 Connected to Hardhat:", w3.is_connected())

# ✅ Load contract ABI + address
with open("LoanContract.json") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # replace with your deployed address
contract = w3.eth.contract(address=contract_address, abi=abi)

# ✅ Use first account as sender
account = w3.eth.accounts[0]

# 1. Store loan (say ML predicted "Rejected")
tx_hash = contract.functions.storeLoan(5000, 12, "Rejected").transact({"from": account})
w3.eth.wait_for_transaction_receipt(tx_hash)
print("✅ Loan decision stored on blockchain!")

# 2. Fetch loan back
loan = contract.functions.getLoan(0).call()
print("📜 Loan from blockchain:", loan)
