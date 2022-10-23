from django.db import models


class BotUser(models.Model):
    tg_id = models.PositiveBigIntegerField(primary_key=True)  # telegram id
    username = models.CharField(max_length=256, unique=True)
    chosen_name = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    state = models.IntegerField()

    gender_choices = (
        ('f', 'Жіноча'),
        ('m', 'Чоловіча'),
        ('o', 'Інша'),
    )

    gender = models.CharField(max_length=1, choices=gender_choices)

    def __str__(self):
        return self.username

    @property
    def gender_verbose(self):
        return dict(BotUser.gender_choices)[self.gender]


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
