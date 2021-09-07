from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from utils.response_wrapper import ResponseWrapper
from notes.serializers import NotesCreateSerializers, NotesDetailSerializers, NotesShortSerializers
from .models import NoteTag, Notes
from utils.custom_viewset import CustomViewSet
from rest_framework import permissions, status
from django.utils.text import slugify
from .permissions import *


class NotesViewset(CustomViewSet):
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['create', 'update']:
            self.serializer_class = NotesCreateSerializers
        elif self.action in ['list']:
            self.serializer_class = NotesShortSerializers
        else:
            self.serializer_class = NotesDetailSerializers
        return self.serializer_class

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsNoteOwner]
        else:
            permission_classes = [IsNoteReader]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            tags = validated_data.pop('tags')
            tags_qs_list = []
            for tag in tags:
                slugify_tag = slugify(tag, allow_unicode=True)
                note_tag_qs, _ = NoteTag.objects.get_or_create(tag=slugify_tag)
                tags_qs_list.append(note_tag_qs)

            qs = Notes.objects.create(
                created_by=request.user, **validated_data)
            qs.tags.set(tags_qs_list)
            serializer = NotesDetailSerializers(instance=qs)
            return ResponseWrapper(data=serializer.data, msg='created')
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    def update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            tags = validated_data.pop('tags')
            qs = self.get_object()
            if tags:
                tags_qs_list = []
                for tag in tags:
                    slugify_tag = slugify(tag, allow_unicode=True)
                    note_tag_qs, _ = NoteTag.objects.get_or_create(
                        tag=slugify_tag)
                    tags_qs_list.append(note_tag_qs)
                qs.tags.set(tags_qs_list)
            qs = serializer.update(instance=qs, validated_data=validated_data)
            serializer = NotesDetailSerializers(instance=qs)
            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
