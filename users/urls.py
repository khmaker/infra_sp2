# coding=utf-8
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CreateUserAPIView
from .views import GetTokenAPIView
from .views import UsersViewSet

v1_router = DefaultRouter()
v1_router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/email/', CreateUserAPIView.as_view()),
    path('v1/auth/token/', GetTokenAPIView.as_view()), ]
