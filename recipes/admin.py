from django.contrib import admin

from recipes.models import Recipe, Ingredient, IngredientForRecipe

admin.site.register(Ingredient)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2


@admin.register(IngredientForRecipe)
class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'count', 'unit',)
    list_display_links = ('recipe', 'ingredient')
    search_fields = ('recipe__name', 'ingredient__name')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author',)
    list_display_links = ('pk', 'name', 'author',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'author__username']
    list_filter = ('tag',)
    inlines = [IngredientInline, ]
