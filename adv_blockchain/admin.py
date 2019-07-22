from django.contrib import admin
from .models import Block, Transaction

admin.site.register((Block, Transaction))
