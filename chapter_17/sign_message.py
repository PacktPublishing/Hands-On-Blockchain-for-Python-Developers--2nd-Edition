from ape import accounts
from eth_account.messages import encode_defunct
from ape.types.signatures import recover_signer
import os

username = os.environ["ACCOUNT_USERNAME"]
account = accounts.load(username)
password = os.environ["MY_PASSWORD"]
account.set_autosign(True, passphrase=password)

message = encode_defunct(text="Hello Apes!")
signature = account.sign_message(message)
print(signature)

recovered_signer = recover_signer(message, signature)
print(account.address)
print(recovered_signer)
