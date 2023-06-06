from django.urls import reverse
import pytest


class TestNotes:
    @pytest.fixture
    def note_viewset_url(self):
        return "api/notes/notes/"

    @pytest.fixture
    def note_create_data(self):
        return {"notes": "string", "title": "string", "tags": ["string"]}

    def test_unauthorized_create_note(
        self,
        client,
        note_create_data,
        note_viewset_url,
        notes_factory,
        note_tag_factory,
    ):
        # without authentication
        response = client.post("api/notes/notes/", note_create_data)
        assert 404 == response.status_code
