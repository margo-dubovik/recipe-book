from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from tgbot.models import BotUser
from tgbot.models import Recipe
from tgbot.forms import RecipeForm


def homeview(request):
    return render(request, 'admin_panel/admin_panel_home.html')


class BotUsers(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel/bot_users_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bot_users'] = BotUser.objects.all()
        return context


class RecipesList(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel/recipes_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.all()
        return context


class NewRecipe(LoginRequiredMixin, View):
    form_class = RecipeForm
    template_name = 'admin_panel/recipe_template.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'button_text': 'Add Recipe'})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New recipe added!")
            return redirect(reverse('recipes'))
        return render(request, self.template_name, {'form': form})


class EditRecipe(LoginRequiredMixin, View):
    form_class = RecipeForm
    template_name = 'admin_panel/recipe_template.html'

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        form = self.form_class(instance=recipe)
        return render(request, self.template_name, {'form': form, 'button_text': 'Save Changes'})

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        form = self.form_class(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes saved!")
            return redirect(reverse('recipes'))
        return render(request, self.template_name, {'form': form})


class DeleteRecipe(LoginRequiredMixin, View):

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if recipe.photo:
            recipe.photo.delete()
        recipe.delete()
        messages.success(request, "Recipe is deleted")
        return redirect(reverse('recipes'))



