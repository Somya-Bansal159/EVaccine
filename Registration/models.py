from os import truncate
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models import UniqueConstraint

# Create your models here.


class registrants(models.Model):
    city_choices = [
        ('A', (
            ('A1', 'A1'),
            ('A2', 'A2'),
            ('A3', 'A3')
        )
        ),
        ('B', (
            ('B1', 'B1'),
            ('B2', 'B2'),
            ('B3', 'B3')
        )
        ),
        ('C', (
            ('C1', 'C1'),
            ('C2', 'C2'),
            ('C3', 'C3')
        )
        )
    ]
    registrant_id = models.AutoField(
        primary_key=True, verbose_name='Registrant ID')
    username = models.CharField(
        max_length=50, verbose_name='Username', default=None)
    password = models.CharField(max_length=50, default=None)
    name = models.CharField(max_length=50, verbose_name='Name')
    email = models.EmailField(
        max_length=50, verbose_name='Email ID', unique=True, default=None)
    date_of_birth = models.DateField(verbose_name='Date of Birth')
    city = models.CharField(
        max_length=50, verbose_name='city', choices=city_choices)
    gender = models.CharField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], verbose_name='Gender', max_length=50)


class centers(models.Model):
    center_id = models.AutoField(primary_key=True, verbose_name='Center ID')
    state = models.CharField(max_length=50, verbose_name='State')
    city = models.CharField(max_length=50, verbose_name='City')
    center_name = models.CharField(max_length=50, verbose_name='Center Name')
    no_of_covaxin = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='No. of Covaxin left')
    no_of_covishield = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='No. of Covishield left')
    no_of_sputnik = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='No. of Sputnik V left')


class statuses(models.Model):
    status_no = models.PositiveSmallIntegerField(primary_key=True)
    first_slot = models.CharField(max_length=50, default="")
    second_slot = models.CharField(max_length=50, default="")


class time_slots(models.Model):
    slot_no = models.PositiveSmallIntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()


class vaccination_status(models.Model):
    registrant_id = models.OneToOneField(
        registrants, related_name='+', verbose_name='Registrant ID', primary_key=True, on_delete=CASCADE)
    vaccine_name = models.CharField(choices=[('Covaxin', 'Covaxin'), (
        'Covishield', 'Covishield'), ('Sputnik V', 'Sputnik V')], verbose_name='Vaccine', max_length=50)
    center_1 = models.ForeignKey(
        centers, null=True, blank=True, related_name="+", on_delete=CASCADE)
    date_of_1st_dose = models.DateField(
        null=True, blank=True, verbose_name='Date of 1st Dose')
    center_2 = models.ForeignKey(
        centers, null=True, blank=True, related_name='+', on_delete=CASCADE)
    date_of_2nd_dose = models.DateField(
        null=True, blank=True, verbose_name='Date of 2nd Dose')
    booking_status = models.ForeignKey(
        statuses, related_name='+', on_delete=CASCADE)


class vacancies(models.Model):
    id = models.AutoField(primary_key=True)
    center = models.ForeignKey(
        centers, related_name='+', on_delete=CASCADE)
    slot_no = models.ForeignKey(
        time_slots, related_name='+', on_delete=CASCADE)
    empty_slots = models.IntegerField()
