import hashlib
import json
from time import time
from uuid import uuid4

from urllib.parse import urlparse
import requests

from .models import Block, Transaction


class Blockchain(object):
    def __init__(self):
        # Assume chain 0 is the chain
        self.chain = Block.objects.all()
        # self.current_transactions = chain.current_transactions
        breakpoint()
        if self.chain[:1].get() is None:
            self.genesis_block()

    def genesis_block(self):
        """
        Create the genesis block and add it to the chain

        The genesis block is the anchor of the chain.  It must be the
        same for all nodes, or their chains will fail consensus.

        It is normally hard-coded
        """
        block = Block(proof=1, previous_hash=1)
        block.save()

        self.chain.append(block)

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        current_transactions = Transaction.object.filter(executed=False)
        block = Block(transactions=current_transactions,
                      proof=proof,
                      previous_hash=previous_hash)
        block.save()

        # Reset the current list of transactions
        current_transactions.update(executed=True)

        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: <str> Address of the Recipient
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        transaction = Transaction(sender=sender,
                                  recipient=recipient,
                                  amount=amount)
        transaction.save()

        return transaction

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

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof:  Does hash(last_proof, proof) contain 6
        leading zeroes?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == "000000"

    # def valid_chain(self, chain):
    #     """
    #     Determine if a given blockchain is valid

    #     :param chain: <list> A blockchain
    #     :return: <bool> True if valid, False if not
    #     """

    #     last_block = chain[0]
    #     current_index = 1

    #     while current_index < len(chain):
    #         block = chain[current_index]
    #         print(f'{last_block}')
    #         print(f'{block}')
    #         print("\n-------------------\n")
    #         # Check that the hash of the block is correct
    #         if block['previous_hash'] != self.hash(last_block):
    #             return False

    #         # Check that the Proof of Work is correct
    #         if not self.valid_proof(last_block['proof'], block['proof']):
    #             return False

    #         last_block = block
    #         current_index += 1

    #     return True
