from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Имя')
    email = forms.EmailField(max_length=254, label='Адрес электронной почты')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email",)
