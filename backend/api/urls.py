from rest_framework import routers
from backend.api.views import SpecialtyViewSet, DoctorViewSet

"""
Registration of urls available in the application
"""
app_name = 'api'
router = routers.DefaultRouter(trailing_slash=True)

router.register('specialties', SpecialtyViewSet)
router.register('doctors', DoctorViewSet)
# router.register('pictures', PictureViewSet, basename='pictures')

urlpatterns = router.urls
