from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router_v1 = DefaultRouter()
router_v1.register('ingredients', views.IngredientListView,
                   basename='ingredients')

urlpatterns = [
    path('api/', include(router_v1.urls)),
]
