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
    created_by = factory.SubFactory(
        "account_management.tests.factories.UserAccountFactory"
    )
    tags = factory.SubFactory(NoteTagFactory)

    class Meta:
        model = Notes

    @factory.post_generation
    def shared_with(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.shared_with.add(user)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class SharedUnseenNotesFactory(DjangoModelFactory):
    note = factory.SubFactory(NotesFactory)

    class Meta:
        model = SharedUnseenNotes
