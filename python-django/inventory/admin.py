from django.contrib import admin

# Register your models here.

from django.contrib import admin
from inventory.models import User, Fridge, Category, Item

admin.site.register(User)
admin.site.register(Fridge)
admin.site.register(Category)
admin.site.register(Item)