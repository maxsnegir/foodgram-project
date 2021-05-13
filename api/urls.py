from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router_v1 = DefaultRouter()
router_v1.register('ingredients', views.IngredientListView,
                   basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('subscriptions/', views.SubscriptionView.as_view()),
    path('subscriptions/<int:pk>/', views.SubscriptionView.as_view())

]