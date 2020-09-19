from rest_framework import status
from backend.conftest import APIClient, pytest


def test_doctor_view_authorized_request(api_client):
    resp = api_client.get('/api/v1/doctors/')
    assert resp.status_code == status.HTTP_200_OK


@pytest.fixture
def api_client_unauthorized():
    client = APIClient()
    return client


def test_doctor_view_unauthorized_request(api_client_unauthorized):
    resp = api_client_unauthorized.get('/api/v1/doctors/')
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_doctor_not_allowed(api_client):
    resp = api_client.post(
        '/api/v1/doctors/',
        data={
            "crm": 4455,
            "name": "Gregory House"
        },
        format='json'
    )
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
