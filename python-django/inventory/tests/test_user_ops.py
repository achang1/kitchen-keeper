from django.test import TestCase
from graphene.test import Client
from inventory.operations.user_operations import Query, Mutation, CreateUser, UpdateUser, DeleteUser

class UserQueryTests(TestCase):
    def setUp(self):
        pass
