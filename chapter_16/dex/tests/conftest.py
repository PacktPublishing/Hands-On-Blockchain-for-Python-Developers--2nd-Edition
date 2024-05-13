import pytest


@pytest.fixture
def deployer(accounts):
    return accounts[0]

@pytest.fixture
def token(deployer, project):
    return deployer.deploy(project.HelloToken, "Hello", "HEL", 3, 100)

@pytest.fixture
def exchange(deployer, project, token):
    return deployer.deploy(project.DEX, token.address)
