from django.db import models

# Create your models here.

class Fridge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_perishable = models.BooleanField('perishable food', default=True)

class Item(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField('quantity', default=0)
    purchase_date = models.DateTimeField('date purchased')
    expiry_date = models.DateTimeField('expiry date')