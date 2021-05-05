from django.views import generic
from recipes.models import Recipe


class RecipeList(generic.ListView):
    queryset = Recipe.objects.select_related('author').all()
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'


class RecipeDetail(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    queryset = Recipe.objects.prefetch_related('get_ingredients__ingredient'). \
        select_related('author')
