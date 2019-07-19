from django.apps import AppConfig
from .models import Blockchain


class AdvBlockchainConfig(AppConfig):
    name = 'adv_blockchain'
    # Get the blockchain from the database
    # For now, assume there is only one and get that
    # Create it if it doesn't exist
    if Blockchain.objects.all()[:1].get() is None:
        # Create the chain and save it to the DB
        blockchain = Blockchain()
        blockchain.save()
