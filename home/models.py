from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField
from django.db.models.query_utils import PathInfo
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# for booking vaccine slot


class rishuVaccineSlot(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    pincode = models.IntegerField(default="null")
    date = models.CharField(max_length=200)
    vaccine_type = models.CharField(max_length=200)
    min_age_limit = models.IntegerField()
    available_capacity = models.IntegerField()

    class Meta:
        db_table = 'rishuVaccineSlot'


class Member_info_Class(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    uid = models.IntegerField(default="null")
    total_member = models.IntegerField()
    age = models.IntegerField()
    first_booking = models.DateField()
    second_booking = models.DateField()

    class Meta:
        db_table = 'member_info_table'


# for allot vaccine slot
class VaccineSlot(models.Model):
    date = models.DateField()
    city = models.CharField(max_length=50)
    pin_code = models.IntegerField()
    vaccine_12 = models.IntegerField()
    vaccine_18 = models.IntegerField()
    vaccine_45 = models.IntegerField()
    vaccine_60 = models.IntegerField()

    class Meta:
        db_table = 'vaccineslot'


class vaccineBookingClass(models.Model):
    uid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50, default="null")
    pincode = models.IntegerField(default="null")
    phone = models.IntegerField()
    first_dose = models.DateField()
    second_dose = models.DateField()
    first_verification = models.BooleanField(default="False")
    second_verification = models.BooleanField(default="False")

    class Meta:
        db_table = 'vaccine_booking_info'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    no_of_member = models.IntegerField()

    def __str__(self):
        self.user.username
