def test_balances(contract, deployer):
    balance = contract.balances(deployer)
    assert balance == 10000

def test_transfer(contract, deployer, accounts):
    destination_account = accounts[1]
    balance = contract.balances(destination_account)
    assert balance == 0
    balance = contract.balances(deployer)
    assert balance == 10000
    contract.transfer(destination_account, 200, sender=deployer)
    balance = contract.balances(destination_account)
    assert balance == 200
    balance = contract.balances(deployer)
    assert balance == 9800
