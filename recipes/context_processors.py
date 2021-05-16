from .models import ShoppingList
from .shop_list import ShopListSession


def recipes_count(request):
    if request.user.is_authenticated:
        recipes_in_list = ShoppingList.objects.filter(
            user=request.user).count()
    else:
        session = ShopListSession(request)
        recipes_in_list = len(session.sl)
    return {'recipes_in_list': recipes_in_list}
