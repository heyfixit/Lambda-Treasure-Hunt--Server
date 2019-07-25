from django.db import models


class Block(models.Model):
    index = models.AutoField(primary_key=True)
    # Note that using this for the first block will make
    # consensus impossible due to different timestamps
    timestamp = models.DateTimeField(auto_now_add=True)
    transactions = models.ManyToManyField('Transaction', blank=True)
    proof = models.IntegerField()
    previous_hash = models.TextField()


class Transaction(models.Model):
    sender = models.TextField()
    recipient = models.TextField()
    amount = models.FloatField()
    executed = models.BooleanField(default=False)


# class Chain(models.Model):
#     # Adding to database to prevent Heroku sharding problems
#     # that arise when this is in memory alone
#     chain = models.ManyToManyField('Block', blank=True)
#     current_transactions = models.ManyToManyField('Transaction', blank=True)
