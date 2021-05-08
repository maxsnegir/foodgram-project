import django_filters
from django_filters import rest_framework as filters

from recipes.models import Ingredient


class IngredientFilter(django_filters.FilterSet):
    query = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['query', ]
