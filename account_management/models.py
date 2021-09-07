from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            username=username,
            email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class UserAccount(AbstractUser):
    USERS_IN_STATUS_CHOICES = [
        ("ACT", "Active"),
        ("UNV", "Unverified"),
        ("BLK", "Blacked"),
        ("DEL", "Deleted"),
    ]
    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = []
    status = models.CharField(max_length=25,
                              choices=USERS_IN_STATUS_CHOICES, default='ACT')
    objects = UserManager()

    # class Meta(AbstractUser.Meta):
    #     swappable = 'AUTH_USER_MODEL'
    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name', 'username']),
        ]
