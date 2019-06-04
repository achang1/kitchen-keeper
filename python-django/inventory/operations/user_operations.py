import graphene
from inventory.models import User
from inventory.operations.object_types import UserType, UserInput

class Query(graphene.ObjectType):
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


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()