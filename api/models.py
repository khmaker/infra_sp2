from datetime import date
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Genre(models.Model):
    name = models.CharField(max_length=150, verbose_name='name')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='name')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='category')
    genre = models.ManyToManyField(Genre,
                                   verbose_name='genre')
    name = models.CharField(max_length=150, verbose_name='name')
    year = models.IntegerField(
            validators=(MaxValueValidator(date.today().year),),
            verbose_name='year')
    description = models.TextField(max_length=150,
                                   verbose_name='description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='title')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='author')
    text = models.TextField(max_length=500,
                            verbose_name='text')
    score = models.IntegerField(default=0,
                                validators=(MinValueValidator(1),
                                            MaxValueValidator(10)),
                                verbose_name='score')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='publication date')

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='review')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='author')
    text = models.TextField(max_length=500,
                            verbose_name='text')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='publication date')

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
