import pytest


@pytest.fixture
def deployer(accounts):
    return accounts[0]

@pytest.fixture
def marketplace_contract(deployer, project):
    return deployer.deploy(project.NFTMarketplace)

@pytest.fixture
def nft_contract(deployer, project):
    return deployer.deploy(project.HelloNFT)

@pytest.fixture
def mint_nfts(nft_contract, deployer, num_nfts=5):
    for i in range(num_nfts):
        nft_contract.mint(deployer, i, sender=deployer)
    return num_nfts
