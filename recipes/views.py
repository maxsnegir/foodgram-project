from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag, Favorite
from .mixins import IsAuthorMixin, FormValidRecipeMixin
from django.db.models import Exists, OuterRef

User = get_user_model()


class RecipeList(generic.ListView):
    queryset = Recipe.objects.all_with_tags_and_authors()
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = qs.annotate(is_favorite=Exists(Favorite.objects.filter(
                recipe_id=OuterRef('pk'), user=self.request.user)))

        tags = self.request.GET.getlist('tags')
        if tags:
            qs = qs.filter(tag__slug__in=tags)
        return qs


class RecipeDetail(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    queryset = Recipe.objects.select_related('author'). \
        prefetch_related('get_ingredients__ingredient')

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs.annotate(is_favorite=Exists(Favorite.objects.filter(
                recipe_id=OuterRef('pk'), user=self.request.user)))
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
        qs = self.user.recipes.all_with_tags_and_authors().annotate(
            is_favorite=Exists(Favorite.objects.filter(user=self.user,
                                                       recipe_id=OuterRef('pk')
                                                       )))
        tags = self.request.GET.getlist('tags')
        if tags:
            qs = qs.filter(tag__slug__in=tags)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.user
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

        tags = self.request.GET.getlist('tags')
        if tags:
            qs = qs.filter(tag__slug__in=tags)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['favorite_page'] = True
        return context
