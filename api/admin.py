# coding=utf-8
from django.contrib import admin

from api.models import Category
from api.models import Comment
from api.models import Genre
from api.models import Review
from api.models import Title

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Review)
