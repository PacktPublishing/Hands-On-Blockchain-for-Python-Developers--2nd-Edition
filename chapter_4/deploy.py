from web3 import Web3

w3 = Web3(Web3.IPCProvider('/tmp/geth.ipc'))

with open("bytecode.txt") as f:
    bytecode = f.read().strip()

with open("abi.json") as f:
    abi = f.read().strip()

with open("my_keystore/UTC--2023-07-08T18-06-12.161925018Z--a7603e35744ea8d88f5f66f0de7bce24f2bf8f2f") as keyfile:
    encrypted_key = keyfile.read()
    password = "mypassword123"
    deployer_private_key = w3.eth.account.decrypt(encrypted_key, password)

deployer_address = "0xA7603e35744EA8d88F5F66f0dE7bcE24f2Bf8F2f"

contract = w3.eth.contract(abi=abi, bytecode=bytecode)

transaction = contract.constructor().build_transaction({
    'from': deployer_address,
    'nonce': w3.eth.get_transaction_count(deployer_address),
    'gas': 200000,
    'gasPrice': Web3.to_wei('50', 'gwei')
})

signed_transaction = w3.eth.account.sign_transaction(transaction, deployer_private_key)

transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print(transaction_hash)
