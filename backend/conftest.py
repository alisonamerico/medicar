import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.fixture
def create_user(db):
    """
    This fixture is responsable for create user.
    """
    User = get_user_model()
    first_name = 'fulano'
    email = 'foo@email.com'
    password = 'bar'
    user = User.objects.create_user(first_name=first_name, email=email,
                                    password=password)
    return user


@pytest.fixture
def api_client(create_user):
    token = Token.objects.create(user=create_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client
