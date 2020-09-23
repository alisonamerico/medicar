from backend.base.apps import BaseConfig


def test_name_app():
    assert BaseConfig.name == 'base'
