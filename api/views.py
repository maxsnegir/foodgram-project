from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from api.filters import IngredientFilter
from api.serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientListView(ListAPIView, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.filter(draft=False)
    http_method_names = ['get', ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter
