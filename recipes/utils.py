from recipes.models import Ingredient, IngredientForRecipe


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
