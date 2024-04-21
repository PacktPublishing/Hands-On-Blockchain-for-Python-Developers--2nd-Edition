def test_init(vault_contract, deployer):
    assert 0 == vault_contract.totalAssets()

def test_deposit(vault_contract, depositor, token_contract, give_token):
    deposit_amount = 1000
    token_contract.approve(vault_contract, deposit_amount, sender=depositor)

    assert 0 == vault_contract.totalAssets()
    vault_contract.deposit(deposit_amount, sender=depositor)
    assert deposit_amount == vault_contract.totalAssets()
