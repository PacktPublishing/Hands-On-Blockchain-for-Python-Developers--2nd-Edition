from web3 import Web3

w3 = Web3(Web3.IPCProvider('/tmp/geth.ipc'))

with open("my_keystore/UTC--2023-07-08T18-06-12.161925018Z--a7603e35744ea8d88f5f66f0de7bce24f2bf8f2f") as keyfile:
    encrypted_key = keyfile.read()
    password = "mypassword123"
    sender_private_key = w3.eth.account.decrypt(encrypted_key, password)

sender_address = "0xA7603e35744EA8d88F5F66f0dE7bcE24f2Bf8F2f"

recipient_address = Web3.to_checksum_address("0xd30561464ee30ff007e8e1c49aa950448db485bd")

amount = Web3.to_wei(2, 'ether')

transaction = {
    'chainId': 1337,
    'from': sender_address,
    'to': recipient_address,
    'value': amount,
    'gas': 21000,
    'gasPrice': Web3.to_wei('50', 'gwei'),
    'nonce': w3.eth.get_transaction_count(sender_address),
}

signed_transaction = w3.eth.account.sign_transaction(transaction, sender_private_key)

transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print(transaction_hash)
