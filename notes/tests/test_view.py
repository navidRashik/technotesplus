from django.urls import reverse
import pytest
from account_management.models import UserAccount
from account_management.tests.factories import UserAccountFactory
from notes.models import Notes
from .factories import NotesFactory
from utils.base import TestStep
from faker import Faker


class TestNotes:
    @pytest.fixture
    def user(self):
        return UserAccountFactory.create()

    @pytest.fixture
    def notes(self):
        return NotesFactory.create_batch(10)

    @pytest.fixture
    def note_viewset_url(self):
        return "/api/notes/"

    @pytest.fixture
    def note_create_data(self):
        return {
            "notes": Faker().text(),
            "title": Faker().text(),
            "tags": [Faker().word()],
        }

    def test_create_note(
        self,
        client,
        auth_user,
        note_create_data,
        note_viewset_url,
        user,
    ):
        with TestStep("without authentication"):
            response = client.post(note_viewset_url, note_create_data)
            assert 401 == response.status_code
        with TestStep("with authentication"):
            client = auth_user(client, user)
            response = client.post(
                note_viewset_url, data=note_create_data, format="json"
            )
            assert response.status_code == 200
            assert response.json().get("data").get("notes") == note_create_data.get(
                "notes"
            )

    def test_get_note(self, note_viewset_url, user, client, auth_user, notes):
        with TestStep("with authentication checking pagination count"):
            client = auth_user(client, user)
            resp = client.get(note_viewset_url)
            assert resp.status_code == 200
            assert notes.__len__() == resp.json().get("pagination").get("count")
