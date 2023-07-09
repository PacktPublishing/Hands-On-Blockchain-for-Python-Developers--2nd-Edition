# @version ^0.3.0

event Donation:
    donatur: indexed(address)
    amount: uint256

num: uint256

@external
def store(num: uint256):
    self.num = num

@external
def retrieve() -> uint256:
    return self.num

@external
@payable
def donate():
    log Donation(msg.sender, msg.value)
