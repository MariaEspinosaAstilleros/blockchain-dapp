#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import pprint
import os

from web3 import Web3, HTTPProvider

class Transaction:
    '''
    Clase que inicia la transaccion
    '''
    def main(self, argv):
        '''
        Main de la clase
        '''
        w3 = Web3(HTTPProvider('http://localhost:8545'))
        if not w3.isConnected():
            print('Cannot connect to node!')
            sys.exit(1)
        print('Node connected!')

        print('Blockchain size: %s' % w3.eth.blockNumber)
        blockNumber = w3.eth.blockNumber - 1
        if blockNumber < 0:
            print('Blockchain is in the genesis block')
            sys.exit(0)
        block = w3.eth.getBlock(blockNumber)
        try:
            transaction = block['transactions'][0]
        except (KeyError, IndexError):
            print('No transactions found!')
            sys.exit(1)

        receipt = w3.eth.getTransactionReceipt(transaction)
        try:
            contractAddress = receipt['contractAddress']
        except KeyError:
            print('No contract address found!')
            sys.exit(1)
        Ballot = w3.eth.contract(
            address=contractAddress,
            abi=self.loadABI('build/contracts/HelloWorld.json')
        )

        #Obtenemos el propietario
        owner = w3.eth.accounts[0]

        #Creamos una nueva votacion
        voting = Voting(Ballot, w3, owner) 

        return voting

    def loadABI(self, binaryContractFile):
        '''
        Carga el ABI de la transaccion
        '''
        with open(binaryContractFile, 'r') as contents:
            contract = json.load(contents)
        if 'abi' not in contract:
            raise RuntimeError('PTTTTTTTTTRRRRRR!!')
        return contract['abi']

class Voting:
    '''
    Clase para la gestion de las votaciones
    '''

    def __init__(self, Ballot, w3, owner):
        '''
        Constructor
        '''
        self.Ballot = Ballot #obtengo mi objeto Ballot de mi clase Transaction
        self.w3 = w3 
        self.owner = owner

    def run(self):
        '''
        Implementacion del metodo run
        '''
        while True:
            self.menu()
            option=int(input("La opcion del menu elegida es >>"))
            self.switch_option(option)

    def menu(self):
        '''
        Muestra las opciones disponibles a realizar
        '''

        os.system('clear') 

        print(""" 
        Bienvenido al menu de nuestro sistema de votaciones
        ------------------------------------------------------
        Seleccione una opcion:
        1.Añadir candidatos
        2.Mostrar candidatos
        3.Cerrar nominaciones
        4.Cerrar votaciones
        5.Emitir votos
        6.Mostrar ganador votaciones
        7.Salir
        """)

    def switch_option(self, argument):
        '''
        Selecciona la opcion que se introduzca por teclado
        '''
        self.switcher = {
            "1": self.add_candidates(), #añade candidatos
            "2": self.show_candidates(), #muestra candidatos
            "3": self.close_nominations(), #cierra nominaciones
            "4": self.close_voting(), #cierra votaciones
            "5": self.vote_for(), #emite votos
            "6": self.winner_candidate(), #muestra ganador
            "7": self.quit()
            }

        print (self.switcher.get(argument, "Invalid option"))

        return 0

    def add_candidates(self):
        '''
        Añade candidatos a la votacion
        '''
        name = input("Introduzca el nombre del candidato: ")
        print('GAS estimation: %s' % self.Ballot.functions.addCandidates(name).estimateGas())
        txn = self.Ballot.functions.addCandidates(name).transact({'from': self.owner})
        return self.w3.eth.getTransactionReceipt(txn)

    def show_candidates(self):
        '''
        Muestra los candidatos de la votacion
        '''
        print('GAS estimation: %s' % self.Ballot.functions.showCandidates().estimateGas())
        return self.Ballot.functions.showCandidates().call()

    def close_nominations(self):
        '''
        Cierre de nominaciones
        '''
        print('GAS estimation: %s' % self.Ballot.functions.startVoting().estimateGas())
        txn = self.Ballot.functions.startVoting().transact({'from': self.owner})
        return self.w3.eth.getTransactionReceipt(txn)

    def close_voting(self): 
        '''
        Cierre de votaciones
        '''
        print('GAS estimation: %s' % self.Ballot.functions.closeVoting().estimateGas())
        txn = self.Ballot.functions.closeVoting().transact({'from': self.owner})
        return self.w3.eth.getTransactionReceipt(txn)

    def vote_for(self):
        '''
        Realiza las votaciones
        '''
        name_candidate = input("Introduzca el nombre del candidato al que quiere votar: ")
        print('GAS estimation: %s' % self.Ballot.functions.voteFor().estimateGas())
        txn = self.Ballot.functions.voteFor(name_candidate).transact({'from': self.owner})
        return self.w3.eth.getTransactionReceipt(txn)
    
    def winner_candidate(self): 
        '''
        Muestra al ganador de la votacion
        '''
        print('GAS estimation: %s' % self.Ballot.functions.winnerCandidate().estimateGas())
        return self.Ballot.functions.winnerCandidate().call()

    def quit(self):
        '''
        Implementacion de la opcion salir
        '''
        print("")
        print('Cerrando aplicacion...')

        return 0
    
if __name__ == "__main__":
    tx = Transaction()
    sys.exit(tx.main(sys.argv))
