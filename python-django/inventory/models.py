from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user_name

class Storage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    storage_type = models.CharField(max_length=50)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField('quantity', default=0)
    purchase_date = models.DateTimeField('date purchased')
    expiry_date = models.DateTimeField('expiry date')
    perishable = models.BooleanField('perishable food', default=True)

    def __str__(self):
        return self.name