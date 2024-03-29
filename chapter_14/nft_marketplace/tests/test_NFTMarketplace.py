from ape.exceptions import ContractLogicError
import pytest

def test_setNFTPrice(marketplace_contract, nft_contract, mint_nfts, deployer, accounts):
    tokenId = 1
    price = 1000
    marketplace_contract.setNFTPrice(nft_contract.address, tokenId, price, sender=deployer)
    assert marketplace_contract.owners(nft_contract.address, tokenId) == deployer
    assert marketplace_contract.prices(nft_contract.address, tokenId) == price

def test_buyNFT(marketplace_contract, nft_contract, mint_nfts, deployer, accounts):
    tokenId = 1
    price = 1000
    user = accounts[1]
    initial_balance_deployer = deployer.balance
    initial_balance_user = user.balance
    marketplace_contract.setNFTPrice(nft_contract.address, tokenId, price, sender=deployer)
    nft_contract.approve(marketplace_contract.address, tokenId, sender=deployer)
    marketplace_contract.buyNFT(nft_contract.address, tokenId, value=price, sender=user)
    assert marketplace_contract.owners(nft_contract.address, tokenId) == user
    assert marketplace_contract.prices(nft_contract.address, tokenId) == 0
    assert nft_contract.ownerOf(tokenId) == user

def test_proposeNFTPrice(marketplace_contract, nft_contract, mint_nfts, deployer, accounts):
    tokenId = 1
    price = 2000
    user = accounts[1]
    marketplace_contract.proposeNFTPrice(nft_contract.address, tokenId, price, value=price, sender=user)
    assert marketplace_contract.proposals(nft_contract.address, tokenId, user) == price

def test_cancelProposalNFTPrice(marketplace_contract, nft_contract, mint_nfts, deployer, accounts):
    tokenId = 1
    price = 2000
    user = accounts[1]
    marketplace_contract.proposeNFTPrice(nft_contract.address, tokenId, price, value=price, sender=user)
    marketplace_contract.cancelProposalNFTPrice(nft_contract.address, tokenId, sender=user)
    assert marketplace_contract.proposals(nft_contract.address, tokenId, user) == 0

def test_acceptNFTProposal(marketplace_contract, nft_contract, mint_nfts, deployer, accounts):
    tokenId = 1
    price = 2000
    user = accounts[1]
    nft_contract.approve(marketplace_contract.address, tokenId, sender=deployer)
    marketplace_contract.proposeNFTPrice(nft_contract.address, tokenId, price, value=price, sender=user)
    marketplace_contract.acceptNFTProposal(nft_contract.address, tokenId, user, sender=deployer)
    assert marketplace_contract.owners(nft_contract.address, tokenId) == user
    assert nft_contract.ownerOf(tokenId) == user
