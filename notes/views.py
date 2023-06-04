from django.utils.text import slugify
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from notes.serializers import (
    NotesCreateSerializers,
    NotesDetailSerializers,
    NotesShortSerializers,
    ShareNoteSerialzier,
)
from utils.custom_viewset import CustomViewSet
from utils.response_wrapper import CustomRenderer, ResponseWrapper

from .models import Notes, NoteTag, SharedUnseenNotes
from .permissions import *


class NotesViewset(CustomViewSet):
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["create", "update"]:
            self.serializer_class = NotesCreateSerializers
        elif self.action in ["list"]:
            self.serializer_class = NotesShortSerializers
        else:
            self.serializer_class = NotesDetailSerializers
        return self.serializer_class

    def get_permissions(self):
        permission_classes = []
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsNoteOwner]
        else:
            permission_classes = [IsNoteReader]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            tags = validated_data.pop("tags")
            tags_qs_list = []
            for tag in tags:
                slugify_tag = slugify(tag, allow_unicode=True)
                note_tag_qs, _ = NoteTag.objects.get_or_create(tag=slugify_tag)
                tags_qs_list.append(note_tag_qs)

            qs = Notes.objects.create(created_by=request.user, **validated_data)
            qs.tags.set(tags_qs_list)
            serializer = NotesDetailSerializers(instance=qs)
            return ResponseWrapper(data=serializer.data, msg="created")
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            tags = validated_data.pop("tags")
            qs = self.get_object()
            if tags:
                tags_qs_list = []
                for tag in tags:
                    slugify_tag = slugify(tag, allow_unicode=True)
                    note_tag_qs, _ = NoteTag.objects.get_or_create(tag=slugify_tag)
                    tags_qs_list.append(note_tag_qs)
                qs.tags.set(tags_qs_list)
            qs = serializer.update(instance=qs, validated_data=validated_data)
            serializer = NotesDetailSerializers(instance=qs)
            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)


class ShareNotesViewset(GenericViewSet):
    http_method_names = ["put", "get"]
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShareNoteSerialzier
    renderer_classes = [CustomRenderer]

    def get_permissions(self):
        permission_classes = []
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsNoteOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id_list = serializer.validated_data.get("user_id_list")
        instance = self.get_object()
        unseen_notes_usr_pk_list = set(user_id_list) - set(
            instance.shared_with.values_list("pk", flat=True)
        )
        obj_list = []
        for usr_pk in unseen_notes_usr_pk_list:
            obj_list.append(SharedUnseenNotes(shared_to_id=usr_pk, note=instance))
        if unseen_notes_usr_pk_list:
            SharedUnseenNotes.objects.bulk_create(
                objs=obj_list,
                batch_size=len(unseen_notes_usr_pk_list),
                ignore_conflicts=True,
            )
        instance.shared_with.set(user_id_list)
        return Response(status=status.HTTP_200_OK)


class MarkAsRead(GenericViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("note_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ]
    )
    def create(self, request):
        note_id = request.query_params.get("note_id")
        qs = SharedUnseenNotes.objects.filter(shared_to=request.user, note_id=note_id)
        if qs:
            qs.delete()
        return ResponseWrapper(response_success=True, status=200)
