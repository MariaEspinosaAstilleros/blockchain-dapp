#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Ballot_contract
from web3 import Web3, HTTPProvider

class Vote:
    def __init__(self, votacion_id, owner):
        self.contract_address = votacion_id
        self.web3 = Web3(HTTPProvider('http://localhost:8545'))
        self.ballot = self.web3.eth.contract(abi=Ballot_contract.ABI, address=votacion_id)
        self.owner = owner

    @property
    def address(self):
        return self.contract_address

    @property
    def winner(self):
        return self.ballot.functions.winnerCandidate().call()

    def add_candidate(self, name):
        trans_hash = self.ballot.functions.addCandidate(name).transact({'from': self.owner})
        return self.web3.eth.getTransaction(trans_hash)

    @property
    def candidates(self):
        return self.ballot.functions.showCandidates().call()

    def start_voting(self):
        trans_hash = self.ballot.functions.startVoting().transact({'from': self.owner})
        return self.web3.eth.getTransaction(trans_hash)

    def stop_voting(self):
        trans_hash = self.ballot.functions.closeVoting().transact({'from': self.owner})
        return self.web3.eth.getTransaction(trans_hash)

    def vote(self, candidate):
        trans_hash = self.ballot.functions.voteFor(candidate).transact({'from': self.owner})
        return self.web3.eth.getTransaction(trans_hash)

def new(owner, candidates, fix_candidates=None):
    web3 = Web3(HTTPProvider('http://localhost:8545'))
    ballot = web3.eth.contract(abi=Ballot_contract.ABI, bytecode=Ballot_contract.BYTECODE)
    trans_hash = ballot.constructor(candidates).transact(transaction={'from': owner})
    trans_receipt = web3.eth.waitForTransactionReceipt(trans_hash)
    #print(trans_receipt)
    vote = Vote(trans_receipt.contractAddress, owner)
    if fix_candidates:
        vote.stop_voting()
    
    return vote

def get(voter_account, ballot_id):
    web3 = Web3(HTTPProvider('http://localhost:8545'))
    if not web3.isAddress(ballot_id):
        raise ValueError('ballot id is not a valid contract address')

    return Vote(ballot_id, voter_account)
