# coding=utf-8
from datetime import date

from django.core.validators import MaxValueValidator as MaxVV
from django.core.validators import MinValueValidator as MinVV
from django.db import models
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models import SlugField
from django.db.models import TextField

from users.models import User


class Genre(Model):
    name = CharField(
        max_length=150,
        verbose_name='name'
        )
    slug = SlugField(
        unique=True,
        verbose_name='slug'
        )

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = CharField(
        max_length=150,
        verbose_name='name'
        )
    slug = SlugField(
        unique=True,
        verbose_name='slug'
        )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Title(Model):
    category = ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='category'
        )
    genre = ManyToManyField(
        Genre,
        verbose_name='genre'
        )
    name = CharField(
        max_length=150,
        verbose_name='name'
        )
    year = IntegerField(
        validators=(MaxVV(date.today().year),),
        verbose_name='year'
        )
    description = TextField(
        max_length=150,
        verbose_name='description'
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class Review(Model):
    title = ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title'
        )
    author = ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author'
        )
    text = TextField(
        max_length=500,
        verbose_name='text'
        )
    score = IntegerField(
        default=0,
        validators=(MinVV(1), MaxVV(10)),
        verbose_name='score'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='publication date'
        )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'


class Comment(Model):
    review = ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='review'
        )
    author = ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author'
        )
    text = TextField(
        max_length=500,
        verbose_name='text'
        )
    pub_date = DateTimeField(
        auto_now_add=True,
        verbose_name='publication date'
        )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
