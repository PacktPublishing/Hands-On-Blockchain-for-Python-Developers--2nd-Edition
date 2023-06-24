# @version ^0.3.0

interface Storage:
    def retrieve() -> uint256: view

storage_contract: Storage

@external
def __init__(storage_address: address):
    self.storage_contract = Storage(storage_address)

@external
def call_retrieve() -> uint256:
    return self.storage_contract.retrieve()
