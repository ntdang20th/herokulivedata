from django.db import models
import datetime
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core import settings


#---------------------------------user - patient - doctor - device----------------------------
class Province(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
class District(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
class Ward(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class ShareAddress(models.Model):
    address = models.CharField(max_length=128, blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True)

class Device(models.Model):
    uuid = models.CharField(max_length=128, default='')
    description = models.TextField(max_length=255, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.uuid

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    share_address = models.ForeignKey(ShareAddress, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=255, blank=True, null=True)

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


#---------------------------------unit - sensor - datasending-------------------------
class Unit(models.Model):
    unit_name = models.CharField(default='', max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.unit_name


class Acceleration(models.Model):
    valueX = models.FloatField(default=0)
    valueY = models.FloatField(default=0)
    valueZ = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def getJson(self):
        data = {"name": "Accelaration", "valueX": self.valueX, "valueY": self.valueY, "valueZ": self.valueZ, "unit": self.unit.__str__()}
        return data


class Gyroscope(models.Model):
    valueX = models.FloatField(default=0)
    valueY = models.FloatField(default=0)
    valueZ = models.FloatField(default=0)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def getJson(self):
        data = {"name": "Gyroscope", "valueX": self.valueX, "valueY": self.valueY, "valueZ": self.valueZ, "unit": self.unit.__str__()}
        return data


class Rotation(models.Model):
    rotationX = models.FloatField(default=0)
    rotationY = models.FloatField(default=0)
    rotationZ = models.FloatField(default=0)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def getJson(self):
        data = {"name": "Rotation", "rotationX": self.rotationX, "rotationY": self.rotationY, "rotationZ": self.rotationZ, "unit": self.unit.__str__()}
        return data


class TouchStatus(models.Model):
    status_name = models.CharField(default='', max_length=50)
    description = models.TextField(default='', max_length=200)

    def __str__(self):
        return self.status_name


class Rawdata(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now())
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    touch_status = models.ForeignKey(TouchStatus, on_delete=models.CASCADE)
    acceleration = models.ForeignKey(Acceleration, on_delete=models.CASCADE)
    gyroscope = models.ForeignKey(Gyroscope, on_delete=models.CASCADE)
    rotation = models.ForeignKey(Rotation, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        sensor = [self.acceleration.getJson(), self.gyroscope.getJson(), self.rotation.getJson()]
        data = {'date':  str(self.date), 'UUID': self.device.__str__(), 'Touch': self.touch_status.__str__(), 'data': sensor}
        async_to_sync(channel_layer.group_send)(
            'sensor_consumer_group', {
                'type': 'send_rawdata',
                'value': json.dumps(data),
            }
        )
        super(Rawdata, self).save(*args, **kwargs)


