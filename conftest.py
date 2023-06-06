import pytest
from rest_framework.test import APIClient

from account_management.tests.factories import UserAccountFactory


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """
    Global DB access to all tests.
    :param db:
    :return:
    """
    pass


@pytest.fixture
def client() -> APIClient:
    """
    better off using rest framework's api client instead of built in django test client for pytest
    since we'll be working with developing and testing apis
    :return:
    """
    return APIClient()


@pytest.fixture()
def auth_user():
    def _authenticate(client, user_account_factory):
        client.force_authenticate(user_account_factory)
        return client

    return _authenticate


@pytest.fixture()
def auth_note_owner():
    def _authenticate(client, note_factory):
        auth_user(client, note_factory.created_by)
        return client

    return _authenticate


@pytest.fixture()
def auth_private_note_reader():
    def _authenticate(client, note_factory):
        auth_user(client, note_factory.shared_with.last())
        return client

    return _authenticate
