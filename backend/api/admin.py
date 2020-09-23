from backend.api.views import MedicalAppointment
from backend.api.models import Doctor, Schedule, Specialty
from django.contrib import admin, messages


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'crm')
    list_filter = ('name', 'crm')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_filter = ('day', 'doctor', 'hourlys')

    def save_model(self, request, obj, form, change):
        if Schedule.objects.filter(doctor__id=obj.doctor.id, day__exact=obj.day).exists():
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'There should only be one schedule per day for each doctor!')
        else:
            super(ScheduleAdmin, self).save_model(request, obj, form, change)


@admin.register(MedicalAppointment)
class MedicalAppointment(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'day', 'hourly')

    def has_add_permission(self, request, obj=None):
        return False
