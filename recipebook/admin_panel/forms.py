from django import forms
from django.forms import ModelForm

from admin_panel.models import Recipe


class RecipeForm(ModelForm):
    photo = forms.ImageField(label='Select a photo', required=False)

    class Meta:
        model = Recipe
        fields = ("name", "text", "photo",)
