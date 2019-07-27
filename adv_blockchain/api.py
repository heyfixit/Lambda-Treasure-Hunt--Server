from django.http import JsonResponse
from .models import Block
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from .blockchain import Blockchain

import json


@csrf_exempt
def mine(request):
    # Get the blockchain from the database
    # For now, assume there is only one and get that
    blockchain = Block.objects.all()
    # Determine if proof is valid
    last_block = blockchain.last()
    last_proof = last_block.proof

    body_unicode = request.body.decode('utf-8')
    values = json.loads(body_unicode)

    submitted_proof = values.get('proof')
    id = values.get('id')

    if Blockchain.valid_proof(last_proof, submitted_proof):
        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mine a new coin
        Blockchain.new_transaction(
            sender="0",
            recipient=id,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = Blockchain.hash(last_block)

        block = Blockchain.new_block(submitted_proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block.index,
            'transactions': str(block.transactions),
            'proof': block.proof,
            'previous_hash': block.previous_hash,
        }

        return JsonResponse(response)
    else:
        response = {
            'message': "Proof was invalid or already submitted."
        }
        return JsonResponse(response)

@csrf_exempt
def new_transaction(request):
    # Get the blockchain from the database
    # For now, assume there is only one and get that
    blockchain = Block.objects.all()

    body_unicode = request.body.decode('utf-8')
    values = json.loads(body_unicode)

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400

    # Create a new Transaction
    index = Blockchain.new_transaction(values['sender'],
                                       values['recipient'],
                                       values['amount'])

    # -1 means the transaction failed due to insufficient funds
    if index > 0:
        response = {'message': f'Transaction will be added to Block {index}'}
    else:
        response = {'message': 'ERROR: Sender has insufficient funds'}
    return JsonResponse(response)

@csrf_exempt
def get_balance(request):
    
    body_unicode = request.body.decode('utf-8')
    values = json.loads(body_unicode)
    
    # Check that the required fields are in the POST'ed data
    required = ['user_id']
    if not all(k in values for k in required):
        return 'Missing Values', 400
    user_id = values['user_id']
    balance = Blockchain.get_user_balance(user_id)

    response = {'message': f'User {user_id} has a balance of {balance}'}
    return JsonResponse(response)


def full_chain(request):
    # Get the blockchain from the database
    # For now, assume there is only one and get that
    blockchain = Block.objects.all()

    data = serializers.serialize('json', blockchain)

    return JsonResponse(data, safe=False)


def last_proof(request):
    # Get the blockchain from the database
    # For now, assume there is only one and get that
    blockchain = Block.objects.all()

    last_proof_value = blockchain.last().proof
    response = {
        'proof': last_proof_value,
        'difficulty': 6
    }
    return JsonResponse(response)
