def test_ownerOf(contract, deployer):
    for i in range(10):
        assert deployer == contract.ownerOf(i)

def test_transfer(contract, deployer, accounts):
    destination_account = accounts[1]
    tokenId = 2
    contract.transfer(tokenId, destination_account, sender=deployer)
    assert destination_account == contract.ownerOf(tokenId)
    for i in range(2):
        assert deployer == contract.ownerOf(i)
    for i in range(3, 10):
        assert deployer == contract.ownerOf(i)
