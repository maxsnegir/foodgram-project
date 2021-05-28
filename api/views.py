from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from api.filters import IngredientFilter
from api.serializers import IngredientSerializer
from recipes.models import Ingredient, Favorite, ShoppingList
from recipes.shop_list import ShopListSession
from users.models import Follow

User = get_user_model()

RESPONSE = JsonResponse({'success': True})
BAD_RESPONSE = JsonResponse({'success': False},
                            status=status.HTTP_400_BAD_REQUEST)


class IngredientListView(generics.ListAPIView, viewsets.ViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.filter(draft=False)
    http_method_names = ['get', ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class BaseView(APIView):
    permission_classes = [IsAuthenticated, ]
    model = None
    field = None

    def post(self, request):
        try:
            self.model.objects.create(**{self.field: request.data['id']},
                                      user=request.user)
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE

    def delete(self, request, pk):
        relation = self.model.objects.filter(**{self.field: pk},
                                             user=request.user)
        deleted, _ = relation.delete()
        if deleted:
            return RESPONSE
        return BAD_RESPONSE


class SubscriptionView(BaseView):
    model = Follow
    field = 'author_id'


class FavoriteView(APIView):
    model = Favorite
    field = 'recipe'


class ShoppingListView(BaseView):
    permission_classes = [AllowAny]
    model = ShoppingList
    field = 'recipe_id'

    def post(self, request):
        if request.user.is_authenticated():
            return super().post(request)
        else:
            shop_list = ShopListSession(request)
            shop_list.add(request.data.get('id'))
        return JsonResponse(RESPONSE)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().delete(request, *args, **kwargs)
        else:
            shop_list = ShopListSession(request)
            shop_list.remove(str(kwargs.get('pk')))
        return JsonResponse(RESPONSE)
