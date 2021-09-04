from account_management.models import UserAccount
from django.db import models
from django.db.models.fields import SlugField


class NoteTag(models.Model):
    tag = models.SlugField(max_length=80)

# Create your models here.


class Notes(models.Model):
    notes = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    tags = models.ManyToManyField(NoteTag, blank=True, related_name="notes")
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        to="account_management.UserAccount", on_delete=models.CASCADE, related_name="created_notes")
    shared_with = models.ManyToManyField(
        to="account_management.UserAccount", related_name="accessable_notes", blank=True)


class SharedUnseenNotes(models.Model):
    shared_to = models.ForeignKey(
        to="account_management.UserAccount", on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    note = models.ForeignKey(
        Notes, on_delete=models.CASCADE, related_name="shared_unseen_notess")
    notified_owner = models.BooleanField(default=False)
