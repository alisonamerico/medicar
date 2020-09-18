from backend.conftest import pytest, get_user_model
from rest_framework import status


def test_user_create(db):
    get_user_model().objects.create_user('foo@email.com', 'bar')
    assert get_user_model().objects.count() == 1


def test_auth_register_view_not_allowed_request(api_client):
    resp = api_client.get('/api/v1/auth/register/')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_auth_login_view_not_allowed_request(api_client):
    resp = api_client.get('/api/v1/auth/login/')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
