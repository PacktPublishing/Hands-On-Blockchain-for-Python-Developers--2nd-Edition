import pytest
from ape.exceptions import ContractLogicError


def test_chairperson(contract, deployer):
    chairperson = contract.chairperson()
    assert chairperson == deployer

def test_addProposal(contract, deployer):
    assert contract.amountProposals() == 0
    assert contract.proposals(0).name == ""
    contract.addProposal("beach", sender=deployer)
    assert contract.amountProposals() == 1
    assert contract.proposals(0).name == "beach"

def test_addProposal_fail(contract, accounts):
    with pytest.raises(ContractLogicError):
        contract.addProposal("beach", sender=accounts[1])

def test_giveRightToVote(contract, deployer, accounts):
    user = accounts[1]
    assert contract.voterCount() == 0
    assert contract.voters(user).weight == 0
    contract.giveRightToVote(user, 1, sender=deployer)
    assert contract.voterCount() == 1
    assert contract.voters(user).weight == 1

    power_user = accounts[2]
    assert contract.voters(power_user).weight == 0
    contract.giveRightToVote(power_user, 9, sender=deployer)
    assert contract.voterCount() == 2
    assert contract.voters(power_user).weight == 9

def test_giveRightToVote_fail(contract, deployer, accounts):
    user = accounts[1]
    with pytest.raises(ContractLogicError):
        contract.giveRightToVote(user, 1, sender=accounts[1])

def test_vote(contract, deployer, accounts):
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    user2 = accounts[2]
    contract.giveRightToVote(user, 1, sender=deployer)
    contract.giveRightToVote(user2, 1, sender=deployer)

    assert contract.voters(user).weight == 1
    assert contract.voters(user).voted == False
    assert contract.voters(user).vote == 0
    assert contract.proposals(0).voteCount == 0
    contract.vote(0, sender=user)
    assert contract.proposals(0).voteCount == 1
    assert contract.voters(user).weight == 0
    assert contract.voters(user).voted == True
    assert contract.voters(user).vote == 0

    assert contract.voters(user2).weight == 1
    assert contract.voters(user2).voted == False
    assert contract.voters(user2).vote == 0
    assert contract.proposals(1).voteCount == 0
    contract.vote(1, sender=user2)
    assert contract.proposals(1).voteCount == 1
    assert contract.voters(user2).weight == 0
    assert contract.voters(user2).voted == True
    assert contract.voters(user2).vote == 1

def test_vote_fail(contract, deployer, accounts):
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    contract.giveRightToVote(user, 1, sender=deployer)

    contract.vote(0, sender=user)
    with pytest.raises(ContractLogicError):
        contract.vote(0, sender=user)

def test_winnerName(contract, deployer, accounts):
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user1 = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    contract.giveRightToVote(user1, 1, sender=deployer)
    contract.giveRightToVote(user2, 1, sender=deployer)
    contract.giveRightToVote(user3, 1, sender=deployer)

    contract.vote(0, sender=user1)
    contract.vote(1, sender=user2)
    contract.vote(1, sender=user3)

    assert contract.proposals(0).voteCount == 1
    assert contract.proposals(1).voteCount == 2
    assert contract.winnerName() == "mountain"
