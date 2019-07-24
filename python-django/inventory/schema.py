import graphene
from inventory.operations.user_operations import Query as UserQuery, Mutation as UserMutation
from inventory.operations.item_operations import Query as ItemQuery, Mutation as ItemMutation

class Query(UserQuery, ItemQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, ItemMutation, graphene.ObjectType):
    pass