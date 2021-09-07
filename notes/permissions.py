from notes.models import Notes
from django.db.models import Q
from account_management.models import UserAccount
from rest_framework import permissions

"""
[summary]
        # self.check_object_permissions(request, obj=1) #its id

Returns
-------
[type]
    [description]
"""


class IsNoteOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Not the Note owner.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if not bool(request.user and request.user.is_authenticated):
            return False

        return Notes.objects.filter(
            created_by=request.user).exists()


class IsNoteReader(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Not the Note owner.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if not bool(request.user and request.user.is_authenticated):
            return False

        return Notes.objects.filter(
            Q(shared_with__pk=request.user.pk) | Q(created_by__pk=request.user.pk)).exists()
