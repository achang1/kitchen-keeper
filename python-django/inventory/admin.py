from django.contrib import admin

# Register your models here.

from django.contrib import admin
from inventory.models import User, Storage, Item

admin.site.register(User)
admin.site.register(Storage)
admin.site.register(Item)