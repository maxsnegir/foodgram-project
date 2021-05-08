from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from recipes.forms import RecipeForm
from recipes.models import Recipe
from .mixins import IsAuthorMixin

from .utils import get_ingredients, create_ingredients_for_recipe


class RecipeList(generic.ListView):
    queryset = Recipe.objects.select_related('author').all()
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'


class RecipeDetail(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    queryset = Recipe.objects.select_related('author'). \
        prefetch_related('get_ingredients__ingredient')


class RecipeCreate(LoginRequiredMixin, generic.CreateView):
    form_class = RecipeForm
    template_name = 'recipes/create_edit_recipe.html'

    def form_valid(self, form):
        ingredients = get_ingredients(self.request)
        if not ingredients:
            form.add_error('ingredients', 'Добавьте ингредиенты')
            return self.render_to_response(self.get_context_data(form=form))

        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()

        create_ingredients_for_recipe(recipe, ingredients)

        return HttpResponseRedirect(recipe.get_absolute_url())


class RecipeUpdate(LoginRequiredMixin, IsAuthorMixin,
                   generic.UpdateView):
    form_class = RecipeForm
    queryset = Recipe.objects.prefetch_related('get_ingredients__ingredient')
    template_name = 'recipes/create_edit_recipe.html'

    def form_valid(self, form):
        ingredients = get_ingredients(self.request)
        if not ingredients:
            form.add_error('ingredients', 'Добавьте ингредиенты')
            return self.render_to_response(self.get_context_data(form=form))

        recipe = form.save()
        recipe.get_ingredients.all().delete()

        create_ingredients_for_recipe(recipe, ingredients)

        return HttpResponseRedirect(self.get_object().get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context


class RecipeDelete(LoginRequiredMixin, IsAuthorMixin, generic.DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_delete.html'
    context_object_name = 'recipe'
    success_url = reverse_lazy('recipes:recipes')
