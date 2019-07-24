import graphene
from graphene_django.types import DjangoObjectType
from inventory.models import User, Item


class UserType(DjangoObjectType):
    class Meta:
        model = User

class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    user_name = graphene.String()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

class ItemType(DjangoObjectType):
    class Meta:
        model = Item

class ItemInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    user = graphene.Field(UserInput)
    category = graphene.String()
    quantity = graphene.Int()
    purchase_date = graphene.DateTime()
    expiry_date = graphene.DateTime()
    perishable = graphene.Boolean()