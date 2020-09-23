from rest_framework import serializers

from backend.api.models import Specialty, Doctor, Schedule, MedicalAppointment


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name']


class DoctorSerializer(serializers.ModelSerializer):
    specialty = SpecialtySerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'crm', 'name', 'specialty']


class ScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'doctor', 'day', 'hourlys']


class MedicalAppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = MedicalAppointment
        fields = ['id', 'day', 'hourly', 'scheduling_date', 'doctor']
