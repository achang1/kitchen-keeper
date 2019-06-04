import graphene
from inventory.operations.user_operations import Query as UserQuery, Mutation as UserMutation
from inventory.operations.storage_operations import Query as StorageQuery, Mutation as StorageMutation
from inventory.operations.item_operations import Query as ItemQuery, Mutation as ItemMutation

class Query(UserQuery, StorageQuery, ItemQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, StorageMutation, ItemMutation, graphene.ObjectType):
    pass