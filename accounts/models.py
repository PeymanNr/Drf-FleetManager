import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('Please Set The Username')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    registration_step = models.PositiveIntegerField(default=1)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def validate_username(self):
        pattern = r'^[a-zA-Z ]+$'
        if not re.match(pattern, self.username):
            raise ValueError(
                'Username must contain only lowercase, uppercase and space letters.')
