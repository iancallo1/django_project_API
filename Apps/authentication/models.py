from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model that extends Django's AbstractUser"""
    email = models.EmailField(unique=True)
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username 