from rest_framework import serializers

from backend.api.models import Specialty, Doctor


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ('id', 'name')


class DoctorSerializer(serializers.ModelSerializer):
    specialty = SpecialtySerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ('id', 'crm', 'name', 'specialty')
