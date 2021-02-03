from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsersViewSet, CreateUserAPIView, GetTokenAPIView
    )

v1_router = DefaultRouter()
v1_router.register('users', UsersViewSet, basename='users')


urlpatterns = [
        path('v1/', include(v1_router.urls)),
        path('v1/auth/email/', CreateUserAPIView.as_view()),
        path('v1/auth/token/', GetTokenAPIView.as_view()),
        ]
