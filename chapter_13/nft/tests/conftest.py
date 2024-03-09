import pytest


@pytest.fixture
def deployer(accounts):
    return accounts[0]

@pytest.fixture
def contract(deployer, project):
    return deployer.deploy(project.VerySimpleNFT)

@pytest.fixture
def erc721_contract(deployer, project):
    return deployer.deploy(project.HelloNFT)

@pytest.fixture
def mint_nfts(erc721_contract, deployer, num_nfts=5):
    for i in range(num_nfts):
        erc721_contract.mint(deployer, i, sender=deployer)
    return num_nfts
