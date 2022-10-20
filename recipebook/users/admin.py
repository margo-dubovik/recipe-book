from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BotAdmin, BotUser
from .forms import BotAdminCreationForm, BotAdminChangeForm


class BotAdminAdmin(UserAdmin):
    add_form = BotAdminCreationForm
    form = BotAdminChangeForm
    model = BotAdmin
    list_display = ["username", "email", ]
    search_fields = ('username', "email",)


admin.site.register(BotAdmin, BotAdminAdmin)
admin.site.register(BotUser)
