import factory
from factory.django import DjangoModelFactory
from ..models import UserAccount


class UserAccountFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = UserAccount
