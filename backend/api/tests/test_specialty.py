from backend.api.models import Specialty
from rest_framework import status
from backend.conftest import APIClient, pytest


def test_specialty_view_authorized_request(api_client):
    resp = api_client.get('/api/v1/specialty/')
    assert resp.status_code == status.HTTP_200_OK


@pytest.fixture
def api_client_unauthorized():
    client = APIClient()
    return client


def test_specialty_view_unauthorized_request(api_client_unauthorized):
    resp = api_client_unauthorized.get('/api/v1/specialty/')
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_specialty(api_client):
    resp = api_client.get(
        '/api/v1/specialty/',
        data={
            "id": 1,
            "name": "Clínico Geral"
        },
        format='json'
    )
    assert resp.status_code == status.HTTP_200_OK


def test_create_specialty_not_allowed(api_client):
    resp = api_client.post(
        '/api/v1/specialty/',
        data={
            "name": "Cardiologia"
        },
        format='json'
    )
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.fixture
def specialty():
    api_specialty = Specialty.objects.create()
    return api_specialty


@pytest.fixture
def update_specialty_not_allowed(api_client, specialty):
    resp = api_client.put(
        f'/api/v1/specialty/{specialty.id}/',
        data={
            "id": 1,
            "name": "Pediatra"
        },
        format='json',)
    return resp


def test_update_specialty_not_allowed(update_specialty_not_allowed, specialty):
    # assert update_specialty.data["name"] == specialty.name
    assert update_specialty_not_allowed.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.fixture
def delete_specialty_not_allowed(api_client, specialty):
    resp = api_client.delete(
        f'/api/v1/specialty/{specialty.id}/',
        data={
            "id": 1,
            "name": "Pediatra"
        },
        format='json',)
    return resp


def test_delete_specialty_not_allowed(delete_specialty_not_allowed):
    assert delete_specialty_not_allowed.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
