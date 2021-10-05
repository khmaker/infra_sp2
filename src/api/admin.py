# coding=utf-8
from django.contrib import admin

from api.models import Category, Comment, Genre, Review, Title

admin.site.register((Title, Genre, Category, Comment, Review))
