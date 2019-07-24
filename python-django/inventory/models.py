from django.db import models
from enum import Enum

# Create your models here.
class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((choice.name, choice.value) for choice in cls)

class User(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user_name

class Item(models.Model):
    class ItemCategory(ChoiceEnum):
        DAIRY = 'dairy'
        MEAT = 'meat'
        VEGETABLES_AND_FRUITS = 'vegetables_and_fruits'
        GRAINS = 'grains'
        SNACKS = 'snacks'
        DRINKS = 'drinks'

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=ItemCategory.choices())
    quantity = models.IntegerField('quantity', default=0)
    purchase_date = models.DateTimeField('date purchased')
    expiry_date = models.DateTimeField('expiry date')
    perishable = models.BooleanField('perishable food', default=True)

    def __str__(self):
        return self.name