#pragma version ^0.3.0

balances: public(HashMap[address, uint256])
owner: public(address)

@external
def __init__():
    self.balances[msg.sender] = 10000
    self.owner = msg.sender

@external
def transfer(_to: address, _amount: uint256) -> bool:
    assert self.balances[msg.sender] >= _amount
    self.balances[msg.sender] -= _amount
    self.balances[_to] += _amount
    return True

@external
def mint(_new_supply: uint256):
    assert msg.sender == self.owner
    self.balances[msg.sender] = _new_supply
