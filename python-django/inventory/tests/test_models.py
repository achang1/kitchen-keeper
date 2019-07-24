from django.test import TestCase
from inventory.models import User, Item


class UserTests(TestCase):
    def setUp(self):
        self.testUser = User.objects.create(user_name="jjames", email="jesse@gmail.com", first_name="Jesse", last_name="James")
    
    def testStringOverrride(self):
        self.assertEquals(str(self.testUser), "jjames")


class ItemTests(TestCase):
    def setUp(self):
        pass
