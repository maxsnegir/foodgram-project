from django import forms
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()


class RecipeForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        disabled=True,
        widget=forms.HiddenInput
    )

    class Meta:
        model = Recipe
        fields = ['name', 'tag', 'cook_time', 'description', 'image',
                  'author']
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }
