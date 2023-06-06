# def test(user_account_factory):
#     u = user_account_factory.build(username="navid", password="new")
#     assert u.username == "navid"
from django.urls import reverse
import pytest
from faker import Faker

from account_management.tests.factories import UserAccountFactory


class TestUser:
    @pytest.fixture
    def user_account_generator(self, user_create_data):
        UserAccountFactory.create_batch(10)

    @pytest.fixture
    def user_crud_url(self):
        return reverse("user_crud")

    @pytest.fixture
    def user_create_data(self):
        return {
            "username": Faker().user_name(),
            "password": "string",
            "first_name": Faker().first_name(),
            "last_name": Faker().last_name(),
        }

    def test_urls(self, user_crud_url):
        assert user_crud_url == "/api/auth/user_account/"

    @pytest.mark.django_db
    def test_user_creation(self, client, user_crud_url, user_create_data):
        response = client.post(user_crud_url, data=user_create_data, format="json")
        assert response.status_code == 200
