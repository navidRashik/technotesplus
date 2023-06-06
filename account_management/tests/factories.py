import factory
from factory.django import DjangoModelFactory
from ..models import UserAccount


class UserAccountFactory(DjangoModelFactory):
    class Meta:
        model = UserAccount
