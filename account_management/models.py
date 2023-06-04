from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as usrmgr

from django.db.models.query_utils import Q
# Create your models here.

from django.db.models.query_utils import Q

class UserManager(usrmgr):
    def get_user_suggestions(self,search_params):
        return UserAccount.objects.filter(
            Q(first_name__icontains=search_params) | 
            Q(last_name__icontains=search_params) | 
            Q(username__icontains=search_params))[:20]

    

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
                              choices=USERS_IN_STATUS_CHOICES, default='UNV')
    objects = UserManager()


    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name', 'username']),
        ]
