# coding=utf-8
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_user(self, email, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault('role', User.Roles.admin)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

    class Roles(models.TextChoices):
        admin = 'admin'
        moderator = 'moderator'
        user = 'user'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='biography'
        )
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.user,
        verbose_name='role'
        )
    email = models.EmailField(
        unique=True,
        verbose_name='email'
        )

    def is_admin(self):
        return self.role == self.Roles.admin or self.is_superuser

    def is_moderator(self):
        return self.role == self.Roles.moderator or self.is_staff
