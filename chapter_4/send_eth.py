from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

sender_private_key = "0x65c82117597db8b300fa9ef72f4d487d54a5008a6305a510cc20e5824b4f02b6"

sender_address = "0x500deEDD3136cddF24CEE2e5Cf5503F4Aa83eCfa"

recipient_address = "0x4CA4C9dd641bd1678812338f118ba3a1fde58201"

amount = Web3.to_wei(5, 'ether')

transaction = {
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
