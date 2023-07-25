def test_retrieve(contract):
    num = contract.retrieve.call()
    assert num == 0

def test_store(contract, deployer):
    contract.store(19, sender=deployer)
    num = contract.retrieve.call()
    assert num == 19
