from backend.urls import urlpatterns


def test_urls_len():
    assert 5 == len(urlpatterns)
