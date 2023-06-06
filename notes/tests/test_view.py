from django.urls import reverse
import pytest

from utils.base import TestStep


class TestNotes:
    @pytest.fixture
    def note_viewset_url(self):
        return "api/notes/notes/"

    @pytest.fixture
    def note_create_data(self):
        return {"notes": "string", "title": "string", "tags": ["string"]}

    def test_unauthorized_create_note(self, client, note_create_data, note_viewset_url):
        with TestStep("without authentication"):
            response = client.post(note_viewset_url, note_create_data)
            assert 404 == response.status_code
