from django.urls import path
from . import views

urlpatterns = [
        path('admin-panel', views.homeview, name='home-view'),
        path('admin-panel/bot-users', views.BotUsersList.as_view(), name='bot-users'),
]