from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter
from api.serializers import IngredientSerializer
from recipes.models import Ingredient, Favorite, Recipe, ShoppingList
from recipes.shop_list import ShopListSession
from users.models import Follow

User = get_user_model()


class IngredientListView(generics.ListAPIView, viewsets.ViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.filter(draft=False)
    http_method_names = ['get', ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs.get('pk')
        relation = Follow.objects.filter(user=self.request.user,
                                         author=author_id)
        relation.delete()
        return Response({'success': True})

    def post(self, request):
        author_id = request.data.get('id')
        author = get_object_or_404(User, id=author_id)

        if self.request.user != author:
            Follow.objects.get_or_create(user=request.user, author=author)
        return Response({'success': True})


class FavoriteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        recipe = get_object_or_404(Recipe, id=request.data.get('id'))
        Favorite.objects.get_or_create(user=self.request.user,
                                       recipe=recipe)
        return Response({'success': True})

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        relation = Favorite.objects.filter(user=self.request.user,
                                           recipe=recipe_id)
        relation.delete()
        return Response({'success': True})


class ShoppingListView(APIView):

    def post(self, request):
        recipe_id = request.data.get('id')
        if request.user.is_authenticated:
            ShoppingList.objects.get_or_create(user=self.request.user,
                                               recipe_id=recipe_id)
        else:
            shop_list = ShopListSession(request)
            shop_list.add(recipe_id)
        return Response({'success': True})

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        if request.user.is_authenticated:
            relation = ShoppingList.objects.filter(user=self.request.user,
                                                   recipe=recipe_id)
            relation.delete()
        else:
            shop_list = ShopListSession(request)
            shop_list.remove(str(recipe_id))
        return Response({'success': True})
