from rest_framework.viewsets import GenericViewSet
from account_management.serializers import UserAccountSerializer
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from utils.response_wrapper import ResponseWrapper
from notes.serializers import NotesCreateSerializers, NotesDetailSerializers, NotesShortSerializers
from .models import NoteTag, Notes
from utils.custom_viewset import CustomViewSet
from rest_framework import permissions, status
from django.utils.text import slugify
from .permissions import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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


class ShareNotesViewset(GenericViewSet):
    http_method_names = ['put', 'get']
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsNoteOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            # 'note_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='note_id'),
            'user_id_list': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.TYPE_INTEGER, description='user_id_list')
        }))
    def update(self, request, *args, **kwargs):
        user_id_list = request.data.get('user_id_list')
        instance = self.get_object()
        instance.shared_with.set(user_id_list)
        return ResponseWrapper(status=200)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("name", openapi.IN_QUERY,
                          type=openapi.TYPE_STRING)
    ])
    def retrieve(self, request, *args, **kwargs):
        search_params = request.query_params.get('name')
        usr = UserAccount.objects.filter(
            Q(first_name__icontains=search_params) | Q(last_name__icontains=search_params) | Q(username__icontains=search_params))[:20]
        serializer = UserAccountSerializer(instance=usr, many=True)
        return ResponseWrapper(data=serializer.data, response_success=True, status=200)
