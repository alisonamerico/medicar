from rest_framework import status
from backend.conftest import APIClient, pytest


def test_schedule_view_authorized_request(api_client):
    resp = api_client.get('/api/v1/schedules/')
    assert resp.status_code == status.HTTP_200_OK


@pytest.fixture
def api_client_unauthorized():
    client = APIClient()
    return client


def test_schedule_view_unauthorized_request(api_client_unauthorized):
    resp = api_client_unauthorized.get('/api/v1/schedules/')
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_schedule(api_client):
    resp = api_client.get(
        '/api/v1/schedules/',
        data={
            "id": 2,
            "doctor": {
                "id": 2,
                "crm": 3711,
                "name": "Drauzio Varella",
                "specialty": {
                    "id": 3,
                    "name": "Clínico Geral"
                }
            },
            "day": "2020-09-24",
            "hourlys": [
                "08:00:00",
                "08:30:00",
                "09:30:00"
            ]
        },
        format='json'
    )
    assert resp.status_code == status.HTTP_200_OK


def test_create_schedule_not_allowed(api_client):
    resp = api_client.post(
        '/api/v1/schedules/',
        data={
            "name": "Cardiologia"
        },
        format='json'
    )
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
