import graphene
from graphene_django.types import DjangoObjectType
from inventory.models import User, Storage, Item


class UserType(DjangoObjectType):
    class Meta:
        model = User

class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    user_name = graphene.String()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

class StorageType(DjangoObjectType):
    class Meta:
        model = Storage

class StorageInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    storage_type = graphene.String()
    users = graphene.List(UserInput)

class ItemType(DjangoObjectType):
    class Meta:
        model = Item

class ItemInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    user = graphene.Field(UserInput)
    storage = graphene.Field(StorageInput)
    category = graphene.String()
    quantity = graphene.Int()
    purchase_date = graphene.DateTime()
    expiry_date = graphene.DateTime()
    perishable = graphene.Boolean()