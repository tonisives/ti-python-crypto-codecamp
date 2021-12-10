# https://github.com/PatrickAlphaC/web3_py_simple_storage
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC")))
chain_id = 4
address = os.getenv("RINKEBY_ADDRESS")
private_key = os.getenv("RINKEBY_PRIVATE")

# CREATE CONTRACT
print("Deploying contract")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(address)
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)

# we are signing a tx, that is deploying contract to the blockchain
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# send this signed tx
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# waits for the ack of the command
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed")

# CALL TO CONTRACT
# Working with the contract
# Need Contract Address, Contact ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value. dont make a state change to the chain
# Transact -> Actually make a state change.

# initial value of favoriteNumber
print(simple_storage.functions.retrieve().call())

print("Modifiying contract")
# create the tx
store_tx = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce + 1,
    }
)
# sign the tx
signed_store_txn = w3.eth.account.sign_transaction(store_tx, private_key=private_key)
# send the tx
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# wait for tx receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("updated")
print(simple_storage.functions.retrieve().call())