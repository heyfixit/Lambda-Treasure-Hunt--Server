from django.http import JsonResponse
from .models import Block
from django.core import serializers


def mine(request):
    # Get the blockchain from the database
    # For now, assume there is only one and get that
    blockchain = Block.objects.all()
    # Determine if proof is valid
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    values = request.get_json()
    submitted_proof = values.get('proof')
    id = values.get('id')

    if blockchain.valid_proof(last_proof, submitted_proof):
        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mine a new coin
        blockchain.new_transaction(
            sender="0",
            recipient=id,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        # print('Hash is: ' + str(previous_hash), file=sys.stderr)
        block = blockchain.new_block(submitted_proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return JsonResponse(response)
    else:
        response = {
            'message': "Proof was invalid or already submitted."
        }
        return JsonResponse(response)


def new_transaction(request):
    # Get the blockchain from the database
    # For now, assume there is only one and get that
    blockchain = Block.objects.all()

    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'],
                                       values['recipient'],
                                       values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
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

    last_proof_value = blockchain.last_block.get('proof')
    response = {
        'proof': last_proof_value
    }
    return JsonResponse(response)
