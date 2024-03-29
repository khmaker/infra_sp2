# coding=utf-8
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin()


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin()


class IsStaffOrAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.is_admin()
                    or request.user.is_moderator()
                    or obj.author == request.user)
        return request.method in SAFE_METHODS
