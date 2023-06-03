from account_management.serializers import UserAccountSerializer
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Notes, NoteTag


class NoteTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTag
        fields = ['tag']


class NotesShortSerializers(serializers.ModelSerializer):
    tags = NoteTagSerializer(many=True)

    class Meta:
        model = Notes
        fields = ['title', 'id', "tags",  "created_by", ]
        read_only_fields = ['id', "tags", "created_by", ]


class NotesDetailSerializers(serializers.ModelSerializer):
    tags = NoteTagSerializer(many=True)
    created_by = UserAccountSerializer()

    class Meta:
        model = Notes
        fields = ['notes', 'title', 'id', "tags",
                  "created_at", "created_by", "updated_at"]
        read_only_fields = ['id', "tags",
                            "created_at", "created_by", "updated_at"]


class NotesCreateSerializers(serializers.ModelSerializer):
    tags = serializers.ListSerializer(
        child=serializers.CharField(max_length=80), required=False)

    class Meta:
        model = Notes
        fields = ['notes', 'title', "tags",
                  ]
class ShareNoteSerialzier(serializers.Serializer):
    user_id_list = serializers.ListSerializer(child=serializers.IntegerField())