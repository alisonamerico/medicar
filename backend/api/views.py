from rest_framework.viewsets import ReadOnlyModelViewSet
# from rest_framework.filters import OrderingFilter, SearchFilter

from backend.api.models import Specialty
from backend.api.serializers import SpecialtySerializer


class SpecialtyViewSet(ReadOnlyModelViewSet):
    serializer_class = SpecialtySerializer
    queryset = Specialty.objects.all()
    search_fields = ('name',)
    # filter_backends = (SearchFilter, OrderingFilter)
