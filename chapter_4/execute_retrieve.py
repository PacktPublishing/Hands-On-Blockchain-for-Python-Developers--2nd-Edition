from web3 import Web3

with open("abi.json") as f:
    abi = f.read().strip()

w3 = Web3(Web3.IPCProvider('/tmp/geth.ipc'))

address = "0x8bb44f25E5b25ac14c8A9f5BFAcdFd1a700bA18B"
contract = w3.eth.contract(address=address, abi=abi)

number = contract.functions.retrieve().call()
print(number)
