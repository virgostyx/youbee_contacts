# youbee_contacts/conftest.py

# System libraries

# Third-party libraries
import pytest
from graphene_django.utils.testing import graphql_query

# Django modules
from django.contrib.auth.models import User

# Django apps

#  Current app modules


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


@pytest.fixture
def credentials():
    return {'username': 'virgostyx', 'email': 'virgostyx@gmail.com', 'password': 'test_pa22word'}


@pytest.fixture
def logged_in(client, credentials):
    u = User.objects.create_user(credentials)
    client.force_login(u)
    yield
    client.logout()

