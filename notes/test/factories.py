import factory
from pytest_factoryboy import register
from factory.django import DjangoModelFactory
from ..models import Notes, SharedUnseenNotes, NoteTag


class NotesFactory(DjangoModelFactory):
    shared_with = factory.SubFactory(
        "account_management.test.factories.UserAccountFactory"
    )
    tags = factory.SubFactory()

    class Meta:
        model = Notes


class NoteTagFactory(DjangoModelFactory):
    class Meta:
        model = NoteTag


class SharedUnseenNotesFactory(DjangoModelFactory):
    note = factory.SubFactory(NotesFactory)

    class Meta:
        model = SharedUnseenNotes


register(NotesFactory)  # => note_factory
register(SharedUnseenNotesFactory, _name="shared_note_factory")


def test_factory(note_factory):
    f = note_factory()
    print(f, f.title)
