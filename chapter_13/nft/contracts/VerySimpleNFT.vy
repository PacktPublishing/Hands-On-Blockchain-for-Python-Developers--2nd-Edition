#pragma version ^0.3.0

ownerOf: public(HashMap[uint256, address])

@external
def __init__():
    for i in range(10):
        self.ownerOf[i] = msg.sender

@external
def transfer(tokenId: uint256, destination: address):
    if self.ownerOf[tokenId] == msg.sender:
        self.ownerOf[tokenId] = destination
