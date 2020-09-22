from datetime import date
from django.db import models
from phone_field import PhoneField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField

"""
A model is the single, definitive source of information about your data.
It contains the essential fields and behaviors of the data you’re storing.
Generally, each model maps to a single database table.
"""


class Specialty(models.Model):
    """
    This class contains the representation of the fields in the Specialty table.
    """
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name = 'Specialty'
        verbose_name_plural = 'Specialties'

    def __str__(self):
        """A string representation of the model."""
        return f'{self.id}, {self.name}'


class Doctor(models.Model):
    """
    This class contains the representation of the fields in the Doctor table.
    """
    name = models.CharField(max_length=150)
    crm = models.IntegerField(unique=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    phone = PhoneField(
        blank=True, null=True, max_length=12,
        help_text="Phone number must be in the format: '(DDD) 9XXXX-XXXX'. Only numbers")
    specialty = models.ForeignKey('api.Specialty',
                                  related_name='doctor_specialty', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        """A string representation of the model."""
        return f'{self.name}'


class Schedule(models.Model):
    """
    This class contains the representation of the fields in the Schedule table.
    """

    def validate_past_date(inserted_date):
        if date.today() > inserted_date:
            raise ValidationError("It is not possible to insert a date before the current day!")
        else:
            return inserted_date

    doctor = models.ForeignKey('api.Doctor', related_name='doctor_schedule', on_delete=models.PROTECT)
    day = models.DateField(validators=[validate_past_date])
    hourlys = ArrayField(models.TimeField(),
                         help_text="Add hours according to the example: 09:00,10:30"
                         )

    def save(self, obj, change):
        if Schedule.objects.filter(doctor__id=obj.doctor.id, day__exact=obj.day).exists():
            raise ValidationError(
                'It should not be possible to create more than one schedule for a doctor in the same day!')
        super(Schedule, self).save(obj, change)

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        ordering = ['-day']

    def __str__(self):
        """A string representation of the model."""
        return f'{self.doctor.name}, {self.day}'


class MedicalAppointment(models.Model):
    """
    This class contains the representation of the fields in the MedicalAppointment table.
    """
    day = models.DateField()
    hourly = models.TimeField()
    scheduling_date = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey('api.Doctor', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_appointment')

    def __str__(self):
        return f'{self.doctor.name}'
