from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('subscriptions/', views.SubscriptionsList.as_view(),
         name='subscriptions'),
    path('create-recipe/', views.RecipeCreate.as_view(), name='create-recipe'),
    path('create-recipe/<int:pk>', views.RecipeUpdate.as_view(),
         name='update-recipe'),
    path('<int:pk>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('<int:pk>/delete/', views.RecipeDelete.as_view(),
         name='recipe_delete'),
    path('<str:username>/', views.UserRecipes.as_view(), name='user_recipes'),
    path('', views.RecipeList.as_view(), name='recipes'),
]
