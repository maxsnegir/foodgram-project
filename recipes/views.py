from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.urls import reverse_lazy
from django.views import generic

from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag, ShoppingList
from .mixins import IsAuthorMixin, FormValidRecipeMixin
from .shop_list import ShopListSession
from .utils import filter_qs_by_tags, is_favorite_and_in_shopping_list, \
    get_data_for_shop_list

User = get_user_model()


class RecipeList(generic.ListView):
    queryset = Recipe.objects.all_with_tags_and_authors()
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        if not self.request.user.is_authenticated:
            session = ShopListSession(self.request)
            context['shop_list'] = session.sl.values()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = is_favorite_and_in_shopping_list(qs, self.request.user)

        return filter_qs_by_tags(self.request, qs)


class RecipeDetail(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    queryset = Recipe.objects.select_related('author'). \
        prefetch_related('get_ingredients__ingredient')

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = is_favorite_and_in_shopping_list(qs, self.request.user)
        return qs


class RecipeCreate(LoginRequiredMixin, FormValidRecipeMixin,
                   generic.CreateView):
    form_class = RecipeForm
    template_name = 'recipes/create_edit_recipe.html'

    def get_initial(self):
        return {'author': self.request.user.id}


class RecipeUpdate(LoginRequiredMixin, IsAuthorMixin,
                   FormValidRecipeMixin, generic.UpdateView):
    form_class = RecipeForm
    queryset = Recipe.objects.prefetch_related('get_ingredients__ingredient')
    template_name = 'recipes/create_edit_recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context


class RecipeDelete(LoginRequiredMixin, IsAuthorMixin, generic.DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_delete.html'
    context_object_name = 'recipe'
    success_url = reverse_lazy('recipes:recipes')


class UserRecipes(RecipeList):
    template_name = 'recipes/user_recipes.html'

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        self.user = get_object_or_404(User, username=username)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.user.recipes.all_with_tags_and_authors()
        if self.request.user.is_authenticated:
            qs = is_favorite_and_in_shopping_list(qs, self.request.user)
        return filter_qs_by_tags(self.request, qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.user
        context['author_page'] = True
        return context


class SubscriptionsList(LoginRequiredMixin, generic.ListView):
    context_object_name = 'subscriptions'
    template_name = 'recipes/subscriptions.html'
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        return user.follower.all().select_related('author')


class FavoritesList(LoginRequiredMixin, RecipeList):
    template_name = 'recipes/favorites.html'

    def get_queryset(self):
        qs = Recipe.objects.all_with_tags_and_authors().filter(
            favorite__user=self.request.user)
        return filter_qs_by_tags(self.request, qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['favorite_page'] = True
        print(self.request.session.items())
        return context


class ShopList(generic.ListView):
    template_name = 'recipes/shopping_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Recipe.objects.filter(shoppinglist__user=self.request.user)
        else:
            session = ShopListSession(self.request)
            recipe_ids = session.sl.keys()
            qs = Recipe.objects.filter(id__in=recipe_ids)
        return qs


def delete_recipe_from_list(request, pk):
    if request.user.is_authenticated:
        ShoppingList.objects.filter(user=request.user,
                                    recipe_id=pk).delete()
    else:
        session = ShopListSession(request)
        session.remove(str(pk))
    return redirect(reverse('recipes:shopping_list'))


def shop_list_export_to_pdf(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(shoppinglist__user=request.user)
    else:
        session = ShopListSession(request)
        recipe_ids = session.sl.keys()
        recipes = Recipe.objects.filter(id__in=recipe_ids)

    data = get_data_for_shop_list(recipes)

    response = HttpResponse(data,
                            content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
