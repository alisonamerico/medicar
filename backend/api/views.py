import time
from datetime import date

from django.db.models import Q
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from backend.api.models import Doctor, MedicalAppointment, Schedule, Specialty
from backend.api.serializers import (DoctorSerializer,
                                     MedicalAppointmentSerializer,
                                     ScheduleSerializer, SpecialtySerializer)


class SpecialtyViewSet(ReadOnlyModelViewSet):
    serializer_class = SpecialtySerializer
    queryset = Specialty.objects.all()
    search_fields = ('name',)
    filter_backends = (SearchFilter, OrderingFilter)
    permission_classes = (IsAuthenticated,)


class DoctorViewSet(ReadOnlyModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    search_fields = ('name',)
    filter_backends = (SearchFilter, OrderingFilter)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        specialty = self.request.query_params.getlist('specialty')
        if specialty:
            return queryset.filter(specialty__id__in=specialty)
        return queryset


class ScheduleViewSet(ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        doctor = self.request.query_params.get('doctor')
        specialty = self.request.query_params.get('specialty')
        start_date = self.request.query_params.get('start_date')
        final_date = self.request.query_params.get('data_final')

        if not ((doctor and specialty and start_date and final_date) is None):
            queryset = queryset.filter(
                Q(doctor__in=Doctor.objects.filter(specialty=specialty)) |
                Q(doctor__id=doctor)).filter(day__gte=start_date, day__lte=final_date)
        return queryset

    def get(self, request, *args, **kwargs):
        for schedule in self.get_queryset():
            for hourly in schedule.hourlys:
                if time.strftime("%H:%M:%S") > f'{hourly}' and date.today() >= schedule.day:
                    schedule.hourlys.remove(hourly)
                    schedule.save()

            if date.today() > schedule.day or len(schedule.hourlys) == 0:
                obj_schedule = Schedule.objects.get(id=schedule.id)
                obj_schedule.save()
        schedules = self.get_queryset()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)


class MedicalAppointmentViewSet(ModelViewSet):
    queryset = MedicalAppointment.objects.all()
    serializer_class = MedicalAppointmentSerializer
    filter_backends = (OrderingFilter,)
    allowed_methods = ('GET', 'POST', 'DELETE')
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        for appointment in MedicalAppointment.objects.filter(user__id=request.user.id).all():
            if date.today() >= appointment.day:
                if time.strftime("%H:%M:%S") > f'{appointment.hourly}':
                    obj_appointment = MedicalAppointment.objects.get(id=appointment.id)
                    obj_appointment.save()
        appointments = MedicalAppointment.objects.filter(user__id=request.user.id)
        serializer = MedicalAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        schedule_id = request.data['schedule_id']
        hourly = request.data['hourly'] + ':00'

        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response({
                'message': 'No schedule found!',
                'status': status.HTTP_404_NOT_FOUND
            })
        else:
            for hourly_schedule in schedule.hourlys:
                if hourly == f'{hourly_schedule}':
                    if MedicalAppointment.objects.filter(day=schedule.day, hourly=hourly, user=request.user).exists():
                        return Response({'message': 'There is already an appointment for that day and time!'})
                    else:
                        appointment = MedicalAppointment.objects.create(
                            day=schedule.day,
                            hourly=hourly_schedule,
                            doctor=schedule.doctor,
                            user=request.user
                        )
                        schedule = Schedule.objects.filter(hourlys__contains=[hourly], id=schedule_id)
                        if schedule.exists():
                            schedule_object = schedule.first()
                            schedule_object.hourlys.remove(hourly_schedule)
                            schedule_object.save()
                        serializer = MedicalAppointmentSerializer(appointment)
                        return Response(serializer.data)
        return Response({'message': 'The selected time is not available!'})

    def destroy(self, request, *args, **kwargs):
        appointment = MedicalAppointment.objects.filter(pk=self.kwargs.get(
            'pk'), user=self.request.user).first()
        if appointment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        appointment.user = None
        appointment.save()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'It is not possible to cancel an appointment\
             for another patient or that there is no'
        })
