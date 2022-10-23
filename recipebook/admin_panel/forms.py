from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import BotAdmin


class BotAdminCreationForm(UserCreationForm):
    class Meta:
        model = BotAdmin
        fields = ("username", "email", )


class BotAdminChangeForm(UserChangeForm):
    class Meta:
        model = BotAdmin
        fields = ("username", "email", )
