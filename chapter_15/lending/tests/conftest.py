import pytest


@pytest.fixture
def deployer(accounts):
    return accounts[0]

@pytest.fixture
def borrower(accounts):
    return accounts[1]

@pytest.fixture
def lending_contract(deployer, project, token_contract, borrower):
    loan_amount = 1000
    collateral = 1 * 10 ** 18
    interest = 10
    return deployer.deploy(project.Lending,
                           borrower,
                           token_contract.address,
                           loan_amount,
                           collateral,
                           interest)

@pytest.fixture
def token_contract(deployer, project):
    return deployer.deploy(project.HelloToken, "Hello", "HEL", 3, 100)

@pytest.fixture
def give_token(token_contract, lending_contract, deployer):
    token_amount = 1000
    token_contract.transfer(lending_contract, token_amount, sender=deployer)
