from ape.exceptions import ContractLogicError
import pytest

def test_init(erc721_contract, deployer):
    assert "Hello NFT" == erc721_contract.name()
    assert "HEL" == erc721_contract.symbol()

def test_balanceOf(erc721_contract, deployer, mint_nfts):
    assert 5 == erc721_contract.balanceOf(deployer)

def test_ownerOf(erc721_contract, deployer, mint_nfts):
    for i in range(5):
        assert deployer == erc721_contract.ownerOf(i)

def test_transfer(erc721_contract, deployer, mint_nfts, accounts):
    user = accounts[1]
    nftId = 2
    assert 5 == erc721_contract.balanceOf(deployer)
    assert 0 == erc721_contract.balanceOf(user)
    assert deployer == erc721_contract.ownerOf(nftId)
    erc721_contract.transferFrom(deployer, user, nftId, sender=deployer)
    assert 4 == erc721_contract.balanceOf(deployer)
    assert 1 == erc721_contract.balanceOf(user)
    assert user == erc721_contract.ownerOf(nftId)

def test_approve(erc721_contract, deployer, mint_nfts, accounts):
    user1 = accounts[1]
    user2 = accounts[2]
    nftId = 2
    otherNftId = 3

    assert erc721_contract.getApproved(nftId) == '0x0000000000000000000000000000000000000000'
    assert erc721_contract.getApproved(otherNftId) == '0x0000000000000000000000000000000000000000'
    with pytest.raises(ContractLogicError):
        erc721_contract.transferFrom(deployer, user2, nftId, sender=user1)
        erc721_contract.transferFrom(deployer, user2, otherNftId, sender=user1)

    erc721_contract.approve(user1, nftId, sender=deployer)
    assert erc721_contract.getApproved(nftId) == user1
    assert erc721_contract.getApproved(otherNftId) == '0x0000000000000000000000000000000000000000'

    assert deployer == erc721_contract.ownerOf(nftId)
    erc721_contract.transferFrom(deployer, user2, nftId, sender=user1)
    assert user2 == erc721_contract.ownerOf(nftId)

    with pytest.raises(ContractLogicError):
        erc721_contract.transferFrom(deployer, user2, otherNftId, sender=user1)

def test_setApprovalForAll(erc721_contract, deployer, mint_nfts, accounts):
    user1 = accounts[1]
    user2 = accounts[2]
    nftId = 2
    otherNftId = 3

    with pytest.raises(ContractLogicError):
        erc721_contract.transferFrom(deployer, user2, nftId, sender=user1)
        erc721_contract.transferFrom(deployer, user2, otherNftId, sender=user1)

    erc721_contract.setApprovalForAll(user1, True, sender=deployer)

    assert deployer == erc721_contract.ownerOf(nftId)
    erc721_contract.transferFrom(deployer, user2, nftId, sender=user1)
    assert user2 == erc721_contract.ownerOf(nftId)

    assert deployer == erc721_contract.ownerOf(otherNftId)
    erc721_contract.transferFrom(deployer, user2, otherNftId, sender=user1)
    assert user2 == erc721_contract.ownerOf(otherNftId)
