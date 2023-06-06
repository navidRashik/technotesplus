# fixtures to be accessed globally across all tests can be put here
from pytest_factoryboy import register

from notes.tests.factories import NotesFactory, NoteTagFactory, SharedUnseenNotesFactory

register(NoteTagFactory)
register(NotesFactory)  # => note_factory
register(SharedUnseenNotesFactory, _name="shared_note_factory")
