from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
        path('', views.homeview, name='home-view'),
        path('login/', LoginView.as_view(template_name='admin_panel/login.html'), name="login"),
        path('logout/', LogoutView.as_view(), name="logout"),
        path('bot-users', views.BotUsers.as_view(), name='bot-users'),
        path('recipes', views.RecipesList.as_view(), name='recipes'),
        path('recipes/new', views.NewRecipe.as_view(), name='new-recipe'),
        path('recipes/<int:recipe_id>/edit', views.EditRecipe.as_view(), name='edit-recipe'),
        path('recipes/<int:recipe_id>/delete', views.DeleteRecipe.as_view(), name='delete-recipe'),
]