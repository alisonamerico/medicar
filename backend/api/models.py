from django.db import models
from phone_field import PhoneField
from django.contrib.auth import get_user_model
from datetime import date

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
        blank=True, max_length=12,
        help_text="Phone number must be in the format: '(DDD) 9XXXX-XXXX'. Only numbers")
    specialty = models.ForeignKey('Specialty', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        """A string representation of the model."""
        return f'{self.id}, {self.crm}, {self.name}, {self.specialty}'


class Hourly(models.Model):
    """
    This class contains the representation of the field in the Hourly table.
    """
    hour = models.TimeField(null=False)

    class Meta:
        verbose_name = 'Hourly'
        verbose_name_plural = 'Hourlys'

    def __str__(self):
        """A string representation of the model."""
        return f'{self.hour}'


class Schedule(models.Model):
    """
    This class contains the representation of the fields in the Schedule table.
    """
    doctor = models.ForeignKey('Doctor', on_delete=models.PROTECT)
    day = models.DateField(default=date.today, null=False)
    hourlys = models.ManyToManyField(Hourly)

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'

    def __str__(self):
        """A string representation of the model."""
        return f'{self.id}, {self.day}'


class MedicalAppointment(models.Model):
    """
    This class contains the representation of the fields in the MedicalAppointment table.
    """
    hourly = models.ForeignKey(Hourly, on_delete=models.DO_NOTHING, null=False)
    scheduling_date = models.DateTimeField(auto_now=True)
    schedule = models.ForeignKey('Schedule', on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if self.day is None:
    #         schedule = Schedule.objects.get(pk=self.schedule.id)
    #         self.day = schedule.day.strftime(f'%Y-%m-%d {self.hourly}')
    #     super(MedicalAppointment, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.hourly}'
