from django.db import models
from address.models import *
from core import settings
from doctor.models import Doctor



class Device(models.Model):
    uuid = models.CharField(max_length=128, default='')
    description = models.TextField(max_length=255, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.uuid


class Familiar(models.Model):
    gender_choice = ((0, 'Nữ'), (1, 'Nam'), (2, 'Không rõ'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.IntegerField(choices=gender_choice, default=0)
    birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    share_address = models.ForeignKey(ShareAddress, on_delete=models.CASCADE)

class PatientInfo(models.Model):
    gender_choice = ((0, 'Nữ'), (1, 'Nam'), (2, 'Không rõ'))
    gender = models.IntegerField(choices=gender_choice, default=0)
    birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    share_address = models.ForeignKey(ShareAddress, on_delete=models.CASCADE)

class Patient(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_info = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)

class HasPatientFamiliar(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    familiar = models.ForeignKey(Familiar, on_delete=models.CASCADE)

