import hashlib
import json
from time import time
from uuid import uuid4

from urllib.parse import urlparse
import requests


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.genesis_block()

        # Don't create a block automatically.  If we do,
        # every node will have a different anchor
        # self.new_block(previous_hash=1, proof=99)  # 99 is faster for 1st

    def genesis_block(self):
        """
        Create the genesis block and add it to the chain

        The genesis block is the anchor of the chain.  It must be the
        same for all nodes, or their chains will fail consensus.

        It is normally hard-coded
        """
        block = {
            'index': 1,
            'timestamp': 0,
            'transactions': [],
            'proof': 99,  # 99 is faster for 1st proof gen
            'previous_hash': 1,
        }

        self.chain.append(block)

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def add_block(self, block):
        """
        Add a received Block to the end of the Blockchain

        :param block: <Block> The validated Block sent by another node in the
        network
        """

        # Reset the current list of transactions.  TODO: Handle pending
        # transactions
        self.current_transactions = []

        self.chain.append(block)

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: <str> Address of the Recipient
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the BLock that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm
        - Find a number p' such that hash(pp') contains 6 leading
        zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof:  Multi-ouroborus:  Do the last six characters of
        the last hash matchc the first six characters of the proof?

        IE:  last_hash: ...999123456, new hash 123456888...
        """

        last_hash = hashlib.sha256(str(last_proof).encode()).hexdigest()
        guess = hashlib.sha256(str(proof).encode()).hexdigest()
        return guess[:6] == last_hash[-6:]

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-------------------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True
