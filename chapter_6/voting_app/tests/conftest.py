import pytest


@pytest.fixture
def deployer(accounts):
    return accounts[0]

@pytest.fixture
def contract(deployer, project):
    return deployer.deploy(project.VotingApp)

@pytest.fixture
def delegate_contract(deployer, project):
    return deployer.deploy(project.DelegateVotingApp)
