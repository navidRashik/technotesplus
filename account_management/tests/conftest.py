# fixtures to be accessed globally across all tests can be put here
from pytest_factoryboy import register

from account_management.tests.factories import UserAccountFactory


register(UserAccountFactory)
