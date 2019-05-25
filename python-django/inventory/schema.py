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
        userName = kwargs.get('userName')
        email = kwargs.get('email')

        if id is not None:
            return User.objects.get(pk=id)
        if userName is not None:
            return User.objects.get(userName=userName)
        if email is not None:
            return User.objects.get(email=email)

        return None

# Input Object Types

class UserInput(graphene.InputObjectType):  
    id = graphene.ID()
    userName = graphene.String()
    email = graphene.String()


# Mutations for User


# class UserMutation(graphene.Mutation):
#     class Arguments:
#         userName = graphene.String(required=True)
#         email = graphene.String(required = True)
#         id = graphene.Int(required=True)
    
#     user = graphene.Field(UserType)

#     def mutate(self, info, userName, email, id):
#         user = User.objects.get(pk=id)
#         user.userName = userName
#         user.email = email
#         user.save()
#         # Notice we return an instance of this mutation
#         return UserMutation(user=user)

class CreateUser(graphene.Mutation):  
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_instance = User(userName=input.userName, email=input.email)
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)
    
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, userName, email, id):
        ok = False
        user_instance = User.objects.get(pk=id)
        if user_instance:
            ok = True
            user_instance.userName = userName
            user_instance.email = email
            user_instance.save()
        return UpdateUser(ok=ok, user=None)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
