#pragma version ^0.3.0

interface ERC721_Interface:
    def transferFrom(_from: address, _to: address, _tokenId: uint256): nonpayable
    def ownerOf(_tokenId: uint256) -> address: view

prices: public(HashMap[address, HashMap[uint256, uint256]])

proposals: public(HashMap[address, HashMap[uint256, HashMap[address, uint256]]])

@external
@payable
@nonreentrant("lock")
def buyNFT(nftAddress: address, tokenId: uint256):
    assert self.prices[nftAddress][tokenId] != 0

    assert msg.value >= self.prices[nftAddress][tokenId]

    buyer: address = msg.sender

    nftContract: ERC721_Interface = ERC721_Interface(nftAddress)

    seller: address = nftContract.ownerOf(tokenId)

    nftContract.transferFrom(seller, buyer, tokenId)

    send(seller, self.prices[nftAddress][tokenId])

    if msg.value > self.prices[nftAddress][tokenId]:
        send(buyer, msg.value - self.prices[nftAddress][tokenId])

    self.prices[nftAddress][tokenId] = 0

@external
def setNFTPrice(nftAddress: address, tokenId: uint256, price: uint256):
    nftContract: ERC721_Interface = ERC721_Interface(nftAddress)

    assert nftContract.ownerOf(tokenId) == msg.sender

    self.prices[nftAddress][tokenId] = price

@external
@payable
def proposeNFTPrice(nftAddress: address, tokenId: uint256, proposedPrice: uint256):
    assert msg.value == proposedPrice, "ETH is not same as proposed price"

    self.proposals[nftAddress][tokenId][msg.sender] = proposedPrice

@external
@nonreentrant("lock2")
def cancelProposalNFTPrice(nftAddress: address, tokenId: uint256):
    proposedPrice: uint256 = self.proposals[nftAddress][tokenId][msg.sender]

    assert proposedPrice > 0, "Proposed price is zero"

    self.proposals[nftAddress][tokenId][msg.sender] = 0

    send(msg.sender, proposedPrice)

@external
@nonreentrant("lock3")
def acceptNFTProposal(nftAddress: address, tokenId: uint256, buyer: address):
    nftContract: ERC721_Interface = ERC721_Interface(nftAddress)

    assert nftContract.ownerOf(tokenId) == msg.sender

    assert self.proposals[nftAddress][tokenId][buyer] != 0

    proposedPrice: uint256 = self.proposals[nftAddress][tokenId][buyer]

    nftContract.transferFrom(msg.sender, buyer, tokenId)

    send(msg.sender, proposedPrice)

    self.proposals[nftAddress][tokenId][buyer] = 0

    self.prices[nftAddress][tokenId] = 0
