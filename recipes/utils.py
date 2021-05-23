from django.db.models import Exists, OuterRef
from django.db.models import Sum

from recipes.models import Ingredient, IngredientForRecipe, Favorite, \
    ShoppingList


def get_ingredients(request):
    ingredients = {}
    for key, value in request.POST.items():
        if key.startswith('nameIngredient'):
            idx = key.split('_')[1]
            count = request.POST.get(f'valueIngredient_{idx}')
            ingredients[value] = count

    return ingredients


def create_ingredients_for_recipe(recipe, ingredients):
    for ingredient, count in ingredients.items():
        ing = Ingredient.objects.get_or_create(title=ingredient)[0]
        count = int(count)
        IngredientForRecipe.objects.create(
            recipe=recipe,
            ingredient=ing,
            count=count)


def filter_qs_by_tags(request, queryset):
    tags = request.GET.getlist('tags')
    if tags:
        queryset = queryset.filter(tag__slug__in=tags)
    return queryset


def is_favorite_and_in_shopping_list(qs, user):
    qs = qs.annotate(is_favorite=Exists(Favorite.objects.filter(
        recipe_id=OuterRef('pk'), user=user)))

    qs = qs.annotate(in_list=Exists(ShoppingList.objects.filter(
        recipe_id=OuterRef('pk'), user=user)))

    return qs


def get_data_for_shop_list(recipes):
    all_ingredients = {}
    ingredients = recipes.values(
        'ingredients__title', 'ingredients__dimension').annotate(
        total_amount=Sum('get_ingredients__count'))
    for item in ingredients:
        key = item['ingredients__title'] + ' ' + item['ingredients__dimension']
        value = int(item['total_amount'])

        all_ingredients[key] = all_ingredients.get(key, 0) + value

    data = ""

    for ingredient, count in all_ingredients.items():
        data += f"{ingredient} - {count}\n"

    return data
