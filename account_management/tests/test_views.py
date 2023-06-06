from django.urls import reverse
import pytest
from faker import Faker
from account_management.models import UserAccount
from account_management.tests.factories import UserAccountFactory
from utils.base import TestStep
import logging

logger = logging.getLogger(__name__)


class TestUser:
    @pytest.fixture
    def user_account_generator(self):
        return UserAccountFactory.create_batch(5)

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

    # @pytest.mark.django_db
    def test_user_creation(self, client, user_crud_url, user_create_data):
        with TestStep("Checking if happy path works with create user api"):
            response = client.post(user_crud_url, data=user_create_data, format="json")
            assert response.status_code == 200
        with TestStep("test if created data is correct or not"):
            user_qs = UserAccount.objects.last()
            assert user_qs.first_name == user_create_data.get("first_name")
            assert user_qs.last_name == user_create_data.get("last_name")
            assert user_qs.username == user_create_data.get("username")
        with TestStep("test user creation with duplicate username"):
            response = client.post(user_crud_url, data=user_create_data, format="json")
            assert response.status_code == 400

    # @pytest.mark.django_db
    def test_search_user_api(
        self, auth_user, client, user_create_data, user_account_generator
    ):
        with TestStep("test check search by name provides data or not"):
            client = auth_user(client, user_account_generator[1])
            response = client.get(
                reverse("search_user"),
                {"name": user_account_generator[-1].first_name},
                format="json",
            )
            assert response.status_code == 200
            assert len(response.json().get("data")) >= 1
