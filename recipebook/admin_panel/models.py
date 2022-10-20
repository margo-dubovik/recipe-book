from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=256)
    text = models.TextField()
    photo = models.ImageField(upload_to='recipe_photo', blank=True)

    def __str__(self):
        return self.name

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return None
