from django.shortcuts import render
from django.http import HttpResponse
from inventory.models import Storage, Category, Item
from rest_framework import viewsets
from inventory.serializers import StorageSerializer, CategorySerializer, ItemSerializer

class StorageViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Storage
    """
    queryset = Storage.objects.all().order_by('name')
    serializer_class = StorageSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Category
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Item
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer