from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
        path('admin-panel', views.homeview, name='home-view'),
        path('admin-panel/login/', LoginView.as_view(template_name='admin_panel/login.html'), name="login"),
        path('admin-panel/logout/', LogoutView.as_view(), name="logout"),
        path('admin-panel/bot-users', views.BotUsers.as_view(), name='bot-users'),
        path('admin-panel/recipes', views.RecipesList.as_view(), name='recipes'),
        path('admin-panel/recipes/new', views.NewRecipe.as_view(), name='new-recipe'),
        path('admin-panel/recipes/<int:recipe_id>/edit', views.EditRecipe.as_view(), name='edit-recipe'),
        path('admin-panel/recipes/<int:recipe_id>/delete', views.DeleteRecipe.as_view(), name='delete-recipe'),
]