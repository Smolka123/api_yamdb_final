import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default=uuid.uuid1)

    def __str__(self) -> str:
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default=uuid.uuid1)

    def __str__(self) -> str:
        return self.name
