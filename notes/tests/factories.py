import factory
from factory.django import DjangoModelFactory
from ..models import Notes, SharedUnseenNotes, NoteTag


class NoteTagFactory(DjangoModelFactory):
    class Meta:
        model = NoteTag


class NotesFactory(DjangoModelFactory):
    shared_with = factory.SubFactory(
        "account_management.tests.factories.UserAccountFactory"
    )
    tags = factory.SubFactory(NoteTagFactory)

    class Meta:
        model = Notes


class SharedUnseenNotesFactory(DjangoModelFactory):
    note = factory.SubFactory(NotesFactory)

    class Meta:
        model = SharedUnseenNotes
