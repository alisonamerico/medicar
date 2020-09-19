from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

from backend.api.models import Specialty, Doctor
from backend.api.serializers import SpecialtySerializer, DoctorSerializer


class SpecialtyViewSet(ReadOnlyModelViewSet):
    serializer_class = SpecialtySerializer
    queryset = Specialty.objects.all()
    search_fields = ('name',)
    filter_backends = (SearchFilter, OrderingFilter)


class DoctorViewSet(ReadOnlyModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    search_fields = ('name',)
    filter_backends = (SearchFilter, OrderingFilter)

    def get_queryset(self):
        queryset = self.queryset

        specialty = self.request.query_params.getlist('specialty')
        if specialty:
            return queryset.filter(specialty__id__in=specialty)
        return queryset
