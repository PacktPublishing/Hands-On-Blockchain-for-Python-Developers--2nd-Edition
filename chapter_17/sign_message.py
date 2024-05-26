from ape import accounts
from eth_account.messages import encode_defunct
from ape.types.signatures import recover_signer
import os

username = os.environ["ACCOUNT_USERNAME"]
account = accounts.load(username)
password = os.environ["MY_PASSWORD"]
account.set_autosign(True, passphrase=password)

message = encode_defunct(text="Hello PacktPub!")
signature = account.sign_message(message)
print(f"The address that creates the signature: {account.address}")
print(f"Signature: {signature}")

recovered_signer = recover_signer(message, signature)
print(f"The address that comes from the signature: {recovered_signer}")
