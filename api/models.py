from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    New class CustomUser which is based on AbstractUser.
    Making the email field required and unique.
    """

    class UserRoles(models.TextChoices):
        """
        An iterator that will be used as value variants for the role field.
        """
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    confirmation_code = models.CharField(max_length=75, blank=True)
    email = models.EmailField(unique=True,
                              verbose_name='Адрес электронной почты')
    bio = models.TextField(max_length=750,
                           blank=True,
                           verbose_name='О себе')
    role = models.CharField(max_length=10,
                            choices=UserRoles.choices,
                            default=UserRoles.USER,
                            verbose_name=('Администратор, модератор'
                                          ' или пользователь.'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )

    class Meta:
        ordering = ('username', )
