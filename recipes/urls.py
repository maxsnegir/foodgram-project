from django.urls import path
from .views import RecipeList, RecipeDetail, RecipeCreate

app_name = 'recipes'

urlpatterns = [
    path('', RecipeList.as_view(), name='recipes'),
    path('<int:pk>', RecipeDetail.as_view(), name='recipe_detail'),
    path('create-recipe/', RecipeCreate.as_view(), name='create-recipe'),

]
