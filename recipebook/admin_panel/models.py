from django.contrib.auth.models import AbstractUser
from django.db import models


class BotAdmin(AbstractUser):
    username = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.username



