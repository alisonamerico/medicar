# Generated by Django 3.1.1 on 2020-09-23 01:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medicalappointment',
            options={'verbose_name': 'MedicalAppointment', 'verbose_name_plural': 'MedicalAppointments'},
        ),
    ]
