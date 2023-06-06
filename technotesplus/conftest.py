# fixtures to be accessed globally across all tests can be put here
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from account_management.tests.factories import UserAccountFactory
from notes.tests.factories import NotesFactory, NoteTagFactory, SharedUnseenNotesFactory


@pytest.fixture
def client():
    """
    better off using rest framework's api client instead of built in django test client for pytest
    since we'll be working with developing and testing apis
    :return:
    """
    return APIClient()
