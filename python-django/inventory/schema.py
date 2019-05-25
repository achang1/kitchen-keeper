import graphene
from graphene_django.types import DjangoObjectType
from inventory.models import User, Storage, Item

class UserType(DjangoObjectType):
    class Meta:
        model = User

class StorageType(DjangoObjectType):
    class Meta:
        model = Storage

class ItemType(DjangoObjectType):
    class Meta:
        model = Item

class Query(object):
    all_users = graphene.List(UserType)
    all_storages = graphene.List(StorageType)
    all_items = graphene.List(ItemType)

    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_storages(self, info, **kwargs):
        return Storage.objects.all()

    def resolve_all_items(self, info, **kwargs):
        return Item.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        user_name = kwargs.get('user_name')
        email = kwargs.get('email')

        if id is not None:
            return User.objects.get(pk=id)
        if user_name is not None:
            return User.objects.get(user_name=user_name)
        if email is not None:
            return User.objects.get(email=email)

        return None

# Input Object Types

class UserInput(graphene.InputObjectType):  
    id = graphene.ID()
    user_name = graphene.String()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()


# Mutations for User

class CreateUser(graphene.Mutation):  
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_instance = User(user_name=input.user_name, email=input.email, first_name=input.first_name, last_name=input.last_name)
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)
    
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, user_name, email, id):
        ok = False
        user_instance = User.objects.get(pk=id)
        if user_instance:
            ok = True
            user_instance.user_name = user_name
            user_instance.email = email
            user_instance.save()
        return UpdateUser(ok=ok, user=None)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
