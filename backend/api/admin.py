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
