import graphene
from inventory.models import Storage, User
from inventory.operations.object_types import StorageType, StorageInput

class Query(graphene.ObjectType):
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


class Mutation(graphene.ObjectType):
    create_storage = CreateStorage.Field()
    update_storage = UpdateStorage.Field()
    delete_storage = DeleteStorage.Field()