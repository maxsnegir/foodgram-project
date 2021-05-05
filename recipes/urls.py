from django.urls import path
from .views import RecipeList, RecipeDetail

app_name = 'recipes'

urlpatterns = [
    path('', RecipeList.as_view(), name='recipes'),
    path('<int:pk>', RecipeDetail.as_view(), name='recipe_detail'),

]
