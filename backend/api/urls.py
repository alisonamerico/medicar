from rest_framework import routers
from backend.api.views import SpecialtyViewSet, DoctorViewSet, ScheduleViewSet, MedicalAppointmentViewSet

"""
Registration of urls available in the application
"""
app_name = 'api'
router = routers.DefaultRouter(trailing_slash=True)

router.register('specialties', SpecialtyViewSet)
router.register('doctors', DoctorViewSet)
router.register('schedules', ScheduleViewSet)
router.register('appointments', MedicalAppointmentViewSet)

urlpatterns = router.urls
