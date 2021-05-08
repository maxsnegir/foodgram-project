from django.urls import path
from .views import RecipeList, RecipeDetail, RecipeCreate, RecipeUpdate, \
    RecipeDelete

app_name = 'recipes'

urlpatterns = [
    path('', RecipeList.as_view(), name='recipes'),
    path('<int:pk>', RecipeDetail.as_view(), name='recipe_detail'),
    path('<int:pk>/delete/', RecipeDelete.as_view(), name='recipe_delete'),
    path('create-recipe/', RecipeCreate.as_view(), name='create-recipe'),
    path('create-recipe/<int:pk>', RecipeUpdate.as_view(),
         name='update-recipe'),

]
