import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
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


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default=uuid.uuid1)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-name']


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default=uuid.uuid1)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-name']


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        related_name='genre'
    )
    category = models.ForeignKey(
        Category,
        related_name='category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    rating = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1),
        MaxValueValidator(10)],
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-rating']


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')

    text = models.TextField(verbose_name='Текст отзыва',
                            max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.IntegerField(
        'Оценка', blank=True,
        validators=[MinValueValidator(1, 'Не меньше 1'),
                    MaxValueValidator(10, 'Не больше 10')]
    )
    pub_date = models.DateTimeField(verbose_name='Дата создания',
                                    auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    text = models.TextField(verbose_name='Текст комментария',
                            max_length=300)
    pub_date = models.DateTimeField(verbose_name='Дата создания',
                                    auto_now_add=True)

    def __str__(self):
        return self.review_id

    class Meta:
        ordering = ['-pub_date']
