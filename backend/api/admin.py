from django.contrib import admin

from backend.api import models


@admin.register(models.Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'crm')
    list_filter = ('name', 'crm')


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_filter = ('day', 'doctor', 'hourlys')


# class MedicalAppointmentInline(admin.TabularInline):
#     model = models.MedicalAppointment
#     exclude = ('user', 'day')
