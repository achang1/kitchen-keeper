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


# Input Object Types

class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    user_name = graphene.String()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

class StorageInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    storage_type = graphene.String()
    users = graphene.List(UserInput)

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


# Queries

class Query(object):
    # User queries
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(), user_name=graphene.String(), email=graphene.String())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        user_name = kwargs.get('user_name')
        email = kwargs.get('email')

        if id is not None:
            return User.objects.get(pk=id)
        elif user_name is not None:
            return User.objects.filter(user_name=user_name)
        elif email is not None:
            return User.objects.get(email=email)
        return None

    # Storage queries
    all_storages = graphene.List(StorageType)
    storage = graphene.Field(StorageType, id=graphene.Int())
    storages = graphene.List(StorageType, storage_type=graphene.String())

    def resolve_all_storages(self, info, **kwargs):
        return Storage.objects.all()

    def resolve_storage(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Storage.objects.get(pk=id)
        return None

    def resolve_storages(self, info, **kwargs):
        storage_type = kwargs.get('storage_type')

        if storage_type is not None:
            return Storage.objects.filter(storage_type=storage_type)
        return None


    # Item queries
    all_items = graphene.List(ItemType)
    item = graphene.List(ItemType, id=graphene.Int(), name=graphene.String(), user=graphene.Argument(UserInput),
                          storage=graphene.Argument(StorageInput), category=graphene.String(), quantity=graphene.Int(), 
                          purchase_date=graphene.DateTime(), expiry_date=graphene.DateTime(), perishable=graphene.Boolean())

    def resolve_all_items(self, info, **kwargs):
        return Item.objects.all()

    def resolve_item(self, info, user=None, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        user_name = user.user_name
        user_email = user.email
        category = kwargs.get('category')
        purchase_date = kwargs.get('purchase_date')
        expiry_date = kwargs.get('expiry_date')
        perishable = kwargs.get('perishable')
        
        if id is not None:
            return Item.objects.get(pk=id)
        elif name is not None:
            return Item.objects.get(name=name)
        elif user_name is not None:
            user = User.objects.get(user_name=user_name)
            return Item.objects.filter(user=user)
        elif user_email is not None:
            user = User.objects.get(user_email=user_email)
            return Item.objects.filter(user=user)
        elif category is not None:
            return Item.objects.get(category=category)
        elif purchase_date is not None:
            return Item.objects.get(purchase_date=purchase_date)
        elif expiry_date is not None:
            return Item.objects.get(expiry_date=expiry_date)
        elif perishable is not None:
            return Item.objects.get(perishable=perishable)
        return None

class ItemInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    storage = graphene.ID(StorageInput)
    category = graphene.String()
    quantity = graphene.Int()
    purchase_date = graphene.DateTime()
    expiry_date = graphene.DateTime()

# Mutations for User

class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_instance = User(user_name=input.user_name, email=input.email,
                             first_name=input.first_name, last_name=input.last_name)
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(self, info, id, input=None):
        ok = False
        # TODO: Right now we can only update user by id, should we also be able to update user by
        # retrieving username and email? If so, should they be allowed to update their username
        # and email?
        user_instance = User.objects.get(pk=id)

        if user_instance:
            ok = True
            if (input.user_name):
                user_instance.user_name = input.user_name
            if (input.email):
                user_instance.email = input.email
            if (input.first_name):
                user_instance.first_name = input.first_name
            if (input.last_name):
                user_instance.last_name = input.last_name
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(self, info, id):
        ok = False

        user_instance = User.objects.get(pk=id)
        if user_instance:
            ok = True
            user_instance.delete()
        return DeleteUser(ok=ok)


# Mutations for Storage
class CreateStorage(graphene.Mutation):
    class Arguments:
        input = StorageInput(required=True)

    ok = graphene.Boolean()
    storage = graphene.Field(StorageType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        users = []

        for user_input in input.users:
            # Retrieve user by id, email, or username, since these are unique
            if user_input.id:
                user = User.objects.get(pk=user_input.id)
            elif user_input.user_name:
                user = User.objects.get(user_name=user_input.user_name)
            elif user_input.email:
                user = User.objects.get(email=user_input.email)
            if user is None:
                return CreateStorage(ok=False, storage=None)
            users.append(user)
        storage_instance = Storage(
            name=input.name, storage_type=input.storage_type)
        storage_instance.save()
        storage_instance.users.set(users)
        return CreateStorage(ok=ok, storage=storage_instance)


class UpdateStorage(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = StorageInput(required=True)

    ok = graphene.Boolean()
    storage = graphene.Field(StorageType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        storage_instance = Storage.objects.get(pk=id)
        if storage_instance:
            ok = True
            users = []

            if input.name:
                storage_instance.name = input.name
            if input.storage_type:
                storage_instance.storage_type = input.storage_type
            storage_instance.save()

            if input.users:
                for user_input in input.users:
                    # Retrieve user by id, email, or username, since these are unique
                    if user_input.id:
                        user = User.objects.get(pk=user_input.id)
                    elif user_input.user_name:
                        user = User.objects.get(user_name=user_input.user_name)
                    elif user_input.email:
                        user = User.objects.get(email=user_input.email)
                    if user is None:
                        return UpdateStorage(ok=False, storage=None)
                    users.append(user)
                storage_instance.users.set(users)
            return UpdateStorage(ok=ok, storage=storage_instance)
        return UpdateStorage(ok=ok, storage=None)


class DeleteStorage(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()
    storage = graphene.Field(StorageType)

    @staticmethod
    def mutate(root, info, id):
        ok = False
        storage_instance = Storage.objects.get(pk=id)
        if storage_instance:
            ok = True
            storage_instance.delete()
        return DeleteStorage(ok=ok)

class CreateItem(graphene.Mutation):
    class Arguments:
        input = ItemInput(required=True)

    ok = graphene.Boolean()
    item = graphene.Field(ItemType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True

        user = User.objects.get(pk=input.user.id)
        storage = Storage.objects.get(pk=input.storage.id)
        item_instance = Item(name=input.name, user=user, storage=storage, category=input.category,
                             quantity=input.quantity, purchase_date=input.purchase_date, expiry_date=input.expiry_date, perishable=input.perishable)
        item_instance.save()
        return CreateItem(ok=ok, item=item_instance)


class UpdateItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ItemInput(required=True)

    ok = graphene.Boolean()
    item = graphene.Field(ItemType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        item_instance = Item.objects.get(pk=id)
        user = User.objects.get(pk=input.user.id)
        storage = Storage.objects.get(pk=input.storage.id)

        if item_instance:
            ok = True
            if input.name:
                item_instance.name = input.name
            if input.user:
                item_instance.user = user
            if input.storage:
                item_instance.storage = storage
            if input.category:
                item_instance.category = input.category
            if input.quantity:
                item_instance.quantity = input.quantity
            if input.storage:
                item_instance.purchase_date = input.purchase_date
            if input.storage:
                item_instance.expiry_date = input.expiry_date
            if input.storage:
                item_instance.perishable = input.perishable
            item_instance.save()
            return UpdateItem(ok=ok, item=item_instance)
        return UpdateItem(ok=ok, item=None)


class DeleteItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()
    item = graphene.Field(ItemType)

    @staticmethod
    def mutate(root, info, id):
        ok = False
        item_instance = Item.objects.get(pk=id)
        if item_instance:
            ok = True
            item_instance.delete()
        return DeleteItem(ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_storage = CreateStorage.Field()
    update_storage = UpdateStorage.Field()
    delete_storage = DeleteStorage.Field()
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()
