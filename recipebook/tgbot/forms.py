from django import forms
from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    photo = forms.ImageField(label='Select a photo', required=False)

    class Meta:
        model = Recipe
        fields = ("name", "text", "photo",)
