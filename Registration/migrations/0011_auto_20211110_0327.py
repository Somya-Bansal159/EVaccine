# Generated by Django 3.2.9 on 2021-11-09 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0010_centers_registrants_statuses_time_slots_vacancies_vaccination_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrants',
            name='aadhar_card_no',
        ),
        migrations.RemoveField(
            model_name='registrants',
            name='mobile_no',
        ),
    ]
