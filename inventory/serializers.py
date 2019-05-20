from rest_framework import serializers
from inventory.models import Storage, Category, Item

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('id', 'name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'is_perishable')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'storage', 'category', 'name', 'quantity', 'purchase_date', 'expiry_date')