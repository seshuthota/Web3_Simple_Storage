import json

import streamlit as st
from dotenv import load_dotenv
from solcx import compile_standard
from web3 import Web3
from web3.middleware import geth_poa_middleware

load_dotenv()
URL = "http://127.0.0.1:8545"
CHAIN_ID = 1337
my_address = "0xD05A4FB24c1EB979a2544A609558F50acDDCD817"
private_key = "1e0e33c750fce87d4dfac4baa3a77290d1c66ea7de479b68450a4acb625af8de"

if not private_key:
    print("No Private key found")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
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


def connect_to_web3():
    w3 = Web3(Web3.HTTPProvider(URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print("Connected to Web3")
    return w3


def initialize_contract(w3):
    # Create a contract in python
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get latest transaction
    nonce = w3.eth.getTransactionCount(my_address)
    # 1. Build a transaction
    transaction = SimpleStorage.constructor().buildTransaction(
        {"chainId": CHAIN_ID, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce})

    # 2. Sign a transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

    # 3. Send a transaction
    print("Deploying the contract...")
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    print("Deployed..")

    # Working with the contract, we need:
    # Contract ABI
    # Contract Address
    simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)
    return simple_storage


st.title('Welcome to Simple Storage App!')
w3 = connect_to_web3()
simple_storage = initialize_contract(w3)


def execute_retrieve():
    return simple_storage.functions.retrieve().call()


def add_person(name, favNumber):
    nonce = w3.eth.getTransactionCount(my_address)
    add_person_tx = simple_storage.functions.addPerson(name, int(favNumber)).buildTransaction({
        "chainId": CHAIN_ID, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce
    })
    print("Adding Person to the contract")
    sign_person_tx = w3.eth.account.sign_transaction(add_person_tx, private_key)
    send_person_tx = w3.eth.send_raw_transaction(sign_person_tx.rawTransaction)
    store_person_tx = w3.eth.waitForTransactionReceipt(send_person_tx)
    print("Add Person transaction executed!")
    print(store_person_tx)


def get_peoples():
    return simple_storage.functions.getPeoples().call()
