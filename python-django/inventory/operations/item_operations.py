import graphene
from inventory.models import Item, Storage, User
from inventory.operations.object_types import ItemType, ItemInput, StorageInput, UserInput

class Query(graphene.ObjectType):
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
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()