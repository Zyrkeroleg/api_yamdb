from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=255)
    # year = models.IntegerField(MinValueValidator=1900)
    description = models.TextField()
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name
