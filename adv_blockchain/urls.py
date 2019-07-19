from django.conf.urls import url
from . import api

urlpatterns = [
    # url('init', api.initialize),
    url('mine', api.mine),
    url('new_transaction', api.new_transaction),
    url('full_chain', api.full_chain),
    url('last_proof', api.last_proof)
]
