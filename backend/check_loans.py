from web3 import Web3
import json

# 1. Connect to local Hardhat blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
print("🔗 Connected:", w3.is_connected())

# 2. Load ABI of LoanContract
with open("../blockchain/artifacts/contracts/LoanContract.sol/LoanContract.json") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# 3. Use deployed contract address (replace with your actual one!)
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
contract = w3.eth.contract(address=contract_address, abi=abi)

# 4. Fetch loan details (first loan stored)
try:
    loan = contract.functions.getLoan(0).call()
    print("\n📄 Loan stored in blockchain:")
    print("Borrower:", loan[0])
    print("Amount:", loan[1])
    print("Status:", loan[2])
    print("Description:", loan[3])
except Exception as e:
    print("⚠️ No loan found yet. Submit one from frontend first.")
