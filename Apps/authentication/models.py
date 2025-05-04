from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model that extends Django's AbstractUser"""
    email = models.EmailField(unique=False)
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'authentication_user'

    def __str__(self):
        return self.username

# Update the AUTH_USER_MODEL setting in settings.py to use this model
AUTH_USER_MODEL = 'authentication.User' 