import django.contrib.auth.views as auth_views
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
]
