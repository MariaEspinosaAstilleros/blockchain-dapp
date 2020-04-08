#!/usr/bin/python3
# -*- coding: utf-8 -*-

from web3 import Web3, HTTPProvider
import Ballot

web3 = Web3(HTTPProvider('http://localhost:8545'))
owner = web3.eth.accounts[0]
user = web3.eth.accounts[1]

#web3.geth.personal.unlockAccount(owner, "1234")
#web3.geth.personal.unlockAccount(user, "")

referendum = Ballot.new(owner, ['Pedro', 'Pablo'])
print(referendum.candidates)
referendum.add_candidate('Albert')
print(referendum.candidates)

referendum.start_voting()

same_referendum = Ballot.get(user, referendum.address)
same_referendum.vote('Albert')

referendum.stop_voting()

print('Candidates %s' % referendum.candidates)
print('Winner %s' % referendum.winner)