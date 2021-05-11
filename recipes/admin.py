from django.contrib import admin

from recipes.models import Recipe, Ingredient, IngredientForRecipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'dimension', 'draft']
    list_editable = ['draft']


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2


@admin.register(IngredientForRecipe)
class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'count')
    list_display_links = ('recipe', 'ingredient')
    search_fields = ('recipe__name', 'ingredient__name')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author',)
    list_display_links = ('pk', 'name', 'author',)
    search_fields = ['name', 'author__username']
    list_filter = ('tag',)
    inlines = [IngredientInline, ]
