import graphene
from inventory.models import Item, User
from inventory.operations.object_types import ItemType, ItemInput, UserInput
from django.http import HttpResponseNotFound

class Query(graphene.ObjectType):
    all_items = graphene.List(ItemType)
    item = graphene.List(ItemType, id=graphene.Int(), name=graphene.String(), user=graphene.Argument(UserInput),
                          category=graphene.String(), quantity=graphene.Int(), purchase_date=graphene.DateTime(), 
                          expiry_date=graphene.DateTime(), perishable=graphene.Boolean())

    def resolve_all_items(self, info, **kwargs):
        return Item.objects.all()

    def resolve_item(self, info, user=None, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        category = kwargs.get('category')
        purchase_date = kwargs.get('purchase_date')
        expiry_date = kwargs.get('expiry_date')
        perishable = kwargs.get('perishable')
        
        if id is not None:
            return Item.objects.get(pk=id)
        elif name is not None:
            return Item.objects.filter(name=name)
        elif user is not None:
            try:
                if user.user_name is not None:
                    user = User.objects.get(user_name=user.user_name)
                else:
                    user = User.objects.get(email=user.email)
                return Item.objects.filter(user=user)
            except Exception as e:
                return HttpResponseNotFound("User does not exist.")
        elif category is not None:
            return Item.objects.filter(category=category)
        elif purchase_date is not None:
            return Item.objects.filter(purchase_date=purchase_date)
        elif expiry_date is not None:
            return Item.objects.filter(expiry_date=expiry_date)
        elif perishable is not None:
            return Item.objects.filter(perishable=perishable)
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
        item_instance = Item(name=input.name, user=user, category=input.category,
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

        if item_instance:
            ok = True
            if input.name:
                item_instance.name = input.name
            if input.user:
                item_instance.user = user
            if input.category:
                item_instance.category = input.category
            if input.quantity:
                item_instance.quantity = input.quantity
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