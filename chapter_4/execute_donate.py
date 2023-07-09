from web3 import Web3

with open("abi.json") as f:
    abi = f.read().strip()

w3 = Web3(Web3.IPCProvider('/tmp/geth.ipc'))

account_address = "0xA7603e35744EA8d88F5F66f0dE7bcE24f2Bf8F2f"

with open("my_keystore/UTC--2023-07-08T18-06-12.161925018Z--a7603e35744ea8d88f5f66f0de7bce24f2bf8f2f") as keyfile:
    encrypted_key = keyfile.read()
    password = "mypassword123"
    account_private_key = w3.eth.account.decrypt(encrypted_key, password)

address = "0x8bb44f25E5b25ac14c8A9f5BFAcdFd1a700bA18B"
contract = w3.eth.contract(address=address, abi=abi)

transaction = contract.functions.donate().build_transaction({
    'from': account_address,
    'value': Web3.to_wei('1', 'ether'),
    'nonce': w3.eth.get_transaction_count(account_address),
    'gas': 200000,
    'gasPrice': Web3.to_wei('50', 'gwei')
})

signed_transaction = w3.eth.account.sign_transaction(transaction, account_private_key)

transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print(transaction_hash)
