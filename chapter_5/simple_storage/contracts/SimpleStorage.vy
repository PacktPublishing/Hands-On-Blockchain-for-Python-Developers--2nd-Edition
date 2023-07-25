# @version ^0.3.0

num: uint256

@external
def store(num: uint256):
    self.num = num

@external
def retrieve() -> uint256:
    return self.num
