# coding=utf-8
from django.contrib import admin

from api.models import Category, Comment, Genre, Review, Title

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Review)
