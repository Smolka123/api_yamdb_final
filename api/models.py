from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
User = get_user_model()


class Title (models.Model):
    pass


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
    
    class Meta():
        ordering = ["-pub_date"]


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    comment_text = models.TextField(verbose_name='Текст комментария',
                            max_length=300)
    pub_date = models.DateTimeField(verbose_name='Дата создания',
                                        auto_now_add=True)
    
    def __str__(self):
        return self.review_id
    
    class Meta():
        ordering = ["-pub_date"]


