from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect

from recipes.utils import get_ingredients, create_ingredients_for_recipe


class IsAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        recipe = self.get_object()
        return recipe.author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return redirect(self.get_object().get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class FormValidRecipeMixin:

    def form_valid(self, form):
        ingredients = get_ingredients(self.request)

        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
            return self.render_to_response(self.get_context_data(form=form))

        recipe = form.save()
        recipe.get_ingredients.all().delete()
        create_ingredients_for_recipe(recipe, ingredients)

        return HttpResponseRedirect(recipe.get_absolute_url())
