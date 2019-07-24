import hashlib
import json

from .models import Block, Transaction


class Blockchain(object):
    @staticmethod
    def new_block(proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        current_transactions = Transaction.objects.filter(executed=False)
        block = Block(proof=proof,
                      previous_hash=previous_hash)
        block.save()
        # Need to save first to create index for many-to-many
        block.transactions.set(current_transactions)
        block.save()

        # Reset the current list of transactions
        current_transactions.update(executed=True)

        return block

    @staticmethod
    def new_transaction(sender, recipient, amount):
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

        return Block.objects.all().last().index + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Convert to Dict so same serialization works

        block_dict = {
            'index': block.index,
            'timestamp': str(block.timestamp),
            'transactions': str(block.transactions),
            'proof': block.proof,
            'previous_hash': block.previous_hash,
        }

        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof:  Does hash(last_proof, proof) contain 6
        leading zeroes?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == "000000"
