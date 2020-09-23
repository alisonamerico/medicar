from rest_framework import status
from backend.conftest import APIClient, pytest


def test_medical_appointment_view_authorized_request(api_client):
    resp = api_client.get('/api/v1/appointments/')
    assert resp.status_code == status.HTTP_200_OK


@pytest.fixture
def api_client_unauthorized():
    client = APIClient()
    return client


def test_medical_appointment_view_unauthorized_request(api_client_unauthorized):
    resp = api_client_unauthorized.get('/api/v1/appointments/')
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_medical_appointment(api_client):
    resp = api_client.get(
        '/api/v1/appointments/',
        data={
            "id": 2,
            "day": "2020-09-23",
            "hourly": "16:00:00",
            "scheduling_date": "2020-09-23T17:55:05.978022-03:00",
            "doctor": {
                "id": 1,
                "crm": 2544,
                "name": "Gregory House",
                "specialty": {
                    "id": 1,
                    "name": "Cardiologia"
                }
            }
        },
        format='json'
    )
    assert resp.status_code == status.HTTP_200_OK
