# @version ^0.3.0

struct Voter:
    weight: uint256
    voted: bool
    vote: uint256

struct Proposal:
    name: String[100]
    voteCount: uint256

voters: public(HashMap[address, Voter])
proposals: public(HashMap[uint256, Proposal])
voterCount: public(uint256)
chairperson: public(address)
amountProposals: public(uint256)

NUM_PROPOSALS: constant(uint256) = 3

@external
def __init__():
    self.chairperson = msg.sender
    self.voterCount = 0

@external
def addProposal(_proposalName: String[100]):
    assert msg.sender == self.chairperson
    i: uint256 = self.amountProposals
    self.proposals[i] = Proposal({
        name: _proposalName,
        voteCount: 0
    })
    self.amountProposals += 1

@external
def giveRightToVote(voter: address, _weight: uint256):
    assert msg.sender == self.chairperson
    assert not self.voters[voter].voted
    assert self.voters[voter].weight == 0
    self.voters[voter].weight = _weight
    self.voterCount += 1

@external
def vote(proposal: uint256):
    assert not self.voters[msg.sender].voted
    assert proposal < self.amountProposals

    self.voters[msg.sender].vote = proposal
    self.voters[msg.sender].voted = True

    self.proposals[proposal].voteCount += self.voters[msg.sender].weight
    self.voters[msg.sender].weight = 0

@view
@internal
def _winningProposal() -> uint256:
    winning_vote_count: uint256 = 0
    winning_proposal: uint256 = 0
    j: uint256 = self.amountProposals
    for i in range(NUM_PROPOSALS):
        if self.proposals[i].voteCount > winning_vote_count:
            winning_vote_count = self.proposals[i].voteCount
            winning_proposal = i
    return winning_proposal

@view
@external
def winningProposal() -> uint256:
    return self._winningProposal()

@view
@external
def winnerName() -> String[100]:
    return self.proposals[self._winningProposal()].name
