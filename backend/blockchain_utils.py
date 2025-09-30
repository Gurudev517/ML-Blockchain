from web3 import Web3
import json

# 1. Connect to Hardhat local blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    raise Exception("⚠️ Web3 not connected to Hardhat node!")

# 2. Load ABI
with open("loan_abi.json", "r") as f:
    contract_abi = json.load(f)

# 3. Set deployed contract address (from your deploy log)
contract_address = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"

# 4. Create contract instance
loan_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# 5. Use first Hardhat account as default sender
owner = w3.eth.accounts[0]
