# coding=utf-8
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet
from api.views import CommentViewSet
from api.views import GenreViewSet
from api.views import ReviewViewSet
from api.views import TitleViewSet

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='reviews'
    )
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/'
    'reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
    )
v1_router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [path('v1/', include(v1_router.urls)), ]
