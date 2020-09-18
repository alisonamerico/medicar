from rest_framework import routers
from backend.api.views import SpecialtyViewSet

"""
Registration of urls available in the application
"""
app_name = 'api'
router = routers.DefaultRouter(trailing_slash=True)

router.register('specialty', SpecialtyViewSet)
# router.register('favorites', FavoriteViewSet, basename='favorites')
# router.register('pictures', PictureViewSet, basename='pictures')

urlpatterns = router.urls
