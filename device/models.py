from django.db import models
import datetime
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from patient.models import Device

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
        patient = self.device.patient
        data = {'date':  str(self.date),
                'UUID': self.device.__str__(),
                'Touch': self.touch_status.__str__(),
                'data': sensor}
        async_to_sync(channel_layer.group_send)(
            'sensor_consumer_group', {
                'type': 'send_rawdata',
                'value': json.dumps(data),
            }
        )
        super(Rawdata, self).save(*args, **kwargs)

