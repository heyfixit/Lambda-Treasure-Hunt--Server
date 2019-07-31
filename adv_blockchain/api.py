from django.http import JsonResponse
from .models import Block, ChainDifficulty
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.decorators import api_view

from .blockchain import Blockchain

import json

REWARD_PER_BLOCK = 5


@api_view(["POST"])
def mine(request):
    player = request.user.player
    # Get the blockchain from the database
    # For now, assume there is only one and get that
    blockchain = Block.objects.all()
    # Determine if proof is valid
    last_block = blockchain.last()
    last_proof = last_block.proof

    body_unicode = request.body.decode('utf-8')
    values = json.loads(body_unicode)

    submitted_proof = values.get('proof')
    player_id = player.id

    if Blockchain.valid_proof(last_proof, submitted_proof):
        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mine a new coin
        Blockchain.new_transaction(
            sender="0",
            recipient=player_id,
            amount=REWARD_PER_BLOCK,
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

# def new_transaction(request):
#     player = request.user.player
#     # Get the blockchain from the database
#     # For now, assume there is only one and get that
#     blockchain = Block.objects.all()

#     body_unicode = request.body.decode('utf-8')
#     values = json.loads(body_unicode)

#     # Check that the required fields are in the POST'ed data
#     required = ['sender', 'recipient', 'amount']
#     if not all(k in values for k in required):
#         return 'Missing Values', 400

#     # Create a new Transaction
#     index = Blockchain.new_transaction(values['sender'],
#                                        values['recipient'],
#                                        values['amount'])

#     # -1 means the transaction failed due to insufficient funds
#     if index > 0:
#         response = {'message': f'Transaction will be added to Block {index}'}
#     else:
#         response = {'message': 'ERROR: Sender has insufficient funds'}
#     return JsonResponse(response)

@api_view(["GET"])
def get_balance(request):
    player = request.user.player

    body_unicode = request.body.decode('utf-8')
    values = json.loads(body_unicode)

    # Check that the required fields are in the POST'ed data
    player_id = player.id
    balance = Blockchain.get_user_balance(player_id)

    response = {'message': f'You have a balance of {balance}'}
    return JsonResponse(response)


# @api_view(["GET"])
# def full_chain(request):
#     player = request.user.player
#     # Get the blockchain from the database
#     # For now, assume there is only one and get that
#     blockchain = Block.objects.all()

#     data = serializers.serialize('json', blockchain)

#     return JsonResponse(data, safe=False)


@api_view(["GET"])
def last_proof(request):
    player = request.user.player
    # Get the blockchain from the database
    # For now, assume there is only one and get that
    blockchain = Block.objects.all()

    last_proof_value = blockchain.last().proof
    response = {
        'proof': last_proof_value,
        'difficulty': ChainDifficulty.objects.all().last().difficulty
    }
    return JsonResponse(response)
