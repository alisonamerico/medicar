from backend.api.apps import ApiConfig


def test_name_app():
    assert ApiConfig.name == 'api'
