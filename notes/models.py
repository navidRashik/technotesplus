from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.base import BaseModel


class NotePrivacyType(models.TextChoices):
    PUBLIC = "PUBLIC", _("Public")
    PRIVATE = "PRIVATE", _("Private")


class NoteTag(models.Model):
    tag = models.SlugField(max_length=80)


# Create your models here.


class Notes(BaseModel):
    notes = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    tags = models.ManyToManyField(NoteTag, blank=True, related_name="notes")
    created_by = models.ForeignKey(
        to="account_management.UserAccount",
        on_delete=models.CASCADE,
        related_name="created_notes",
    )
    shared_with = models.ManyToManyField(
        to="account_management.UserAccount", related_name="accessible_notes", blank=True
    )
    note_privacy_type = models.CharField(
        max_length=20, choices=NotePrivacyType.choices, default=NotePrivacyType.PRIVATE
    )


class SharedUnseenNotes(models.Model):
    shared_to = models.ForeignKey(
        to="account_management.UserAccount",
        on_delete=models.CASCADE,
        related_name="shared_unseen_notes",
    )
    shared_at = models.DateTimeField(auto_now_add=True)
    note = models.ForeignKey(
        Notes, on_delete=models.CASCADE, related_name="shared_unseen_notes"
    )
