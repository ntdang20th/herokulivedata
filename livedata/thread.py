import threading
import datetime
import time
import uuid
from channels.layers import get_channel_layer
from device.models import *
from faker import Faker
from asgiref.sync import async_to_sync
import json
import random
import requests

fake = Faker()


class CreateSensorThread(threading.Thread):

    def __init__(self, total):
        self.total = total
        threading.Thread.__init__(self)

    def run(self):
        try:
            print('Sensor Thread Start!')
            channel_layer = get_channel_layer()
            for i in range(self.total):
                acceleration_sensor = Acceleration.objects.create(
                    valueX=random.uniform(-0.09, -0.01),
                    valueY=random.uniform(0.01, 0.09),
                    valueZ=random.uniform(1.01, 1.09),
                    unit=Unit.objects.get(pk=1)
                )
                gyroscope_sensor = Gyroscope.objects.create(
                    valueX=random.uniform(-1.8, -0.2),
                    valueY=random.uniform(12.1, 13),
                    valueZ=random.uniform(12.1, 13),
                    unit=Unit.objects.get(pk=2)
                )
                rotation_sensor = Rotation.objects.create(
                    rotationX=random.uniform(0.9, 16.9),
                    rotationY=random.uniform(0.01, 4.9),
                    rotationZ=random.uniform(-45, 45),
                    unit=Unit.objects.get(pk=3)
                )

                channel_layer = get_channel_layer()
                data = {'date': str(datetime.datetime.now()), 'UUID': str(uuid.uuid4()), 'Touch': 'no touch detected', 'data': [acceleration_sensor.getJson(), gyroscope_sensor.getJson(), rotation_sensor.getJson()]}
                print(data)

                async_to_sync(channel_layer.group_send)(
                    'sensor_consumer_group', {
                        'type': 'send_rawdata',
                        'value': json.dumps(data),
                    }
                )
                time.sleep(1)
        except Exception as e:
            print(e)

class StartSensor1(threading.Thread):
    def run(self):
        try:
            print('Sensor 1 Start!')
            for i in range(60):
                acceleration_sensor = Acceleration.objects.create(
                    valueX=random.uniform(-0.09, -0.01),
                    valueY=random.uniform(0.01, 0.09),
                    valueZ=random.uniform(1.01, 1.09),
                    unit=Unit.objects.get(pk=1)
                )
                gyroscope_sensor = Gyroscope.objects.create(
                    valueX=random.uniform(-1.8, -0.2),
                    valueY=random.uniform(12.1, 13),
                    valueZ=random.uniform(12.1, 13),
                    unit=Unit.objects.get(pk=2)
                )
                rotation_sensor = Rotation.objects.create(
                    rotationX=random.uniform(0.9, 16.9),
                    rotationY=random.uniform(0.01, 4.9),
                    rotationZ=random.uniform(-45, 45),
                    unit=Unit.objects.get(pk=3)
                )
                data = {'date': str(datetime.datetime.now()), 'UUID': 'd1e231bc-8bef-47f9-8383-70b51310a1d9',
                        'Touch': 'no touch detected',
                        'data': [acceleration_sensor.getJson(), gyroscope_sensor.getJson(), rotation_sensor.getJson()]}

                payload_json = json.dumps(data, indent=4)
                headers = {
                    "accept": "text/plain, */*; q=0.01",
                    "accept-language": "en-US,en;q=0.9",
                    "content-type": "application/json; charset=UTF-8"
                }
                url = 'https://livedatawebsocket.herokuapp.com/sensor/post/'

                x = requests.post(url, verify=True, data=payload_json, headers=headers)
                time.sleep(1)
        except Exception as e:
            print(e)

class StartSensor2(threading.Thread):
    def run(self):
        try:
            print('Sensor 1 Start!')
            for i in range(60):
                acceleration_sensor = Acceleration.objects.create(
                    valueX=random.uniform(-0.09, -0.01),
                    valueY=random.uniform(0.01, 0.09),
                    valueZ=random.uniform(1.01, 1.09),
                    unit=Unit.objects.get(pk=1)
                )
                gyroscope_sensor = Gyroscope.objects.create(
                    valueX=random.uniform(-1.8, -0.2),
                    valueY=random.uniform(12.1, 13),
                    valueZ=random.uniform(12.1, 13),
                    unit=Unit.objects.get(pk=2)
                )
                rotation_sensor = Rotation.objects.create(
                    rotationX=random.uniform(0.9, 16.9),
                    rotationY=random.uniform(0.01, 4.9),
                    rotationZ=random.uniform(-45, 45),
                    unit=Unit.objects.get(pk=3)
                )
                data = {'date': str(datetime.datetime.now()), 'UUID': 'bea44629-1aea-4404-b88c-7a0a0519b35d',
                        'Touch': 'no touch detected',
                        'data': [acceleration_sensor.getJson(), gyroscope_sensor.getJson(), rotation_sensor.getJson()]}

                payload_json = json.dumps(data, indent=4)
                headers = {
                    "accept": "text/plain, */*; q=0.01",
                    "accept-language": "en-US,en;q=0.9",
                    "content-type": "application/json; charset=UTF-8"
                }
                url = 'https://livedatawebsocket.herokuapp.com/sensor/post/'

                x = requests.post(url, verify=True, data=payload_json, headers=headers)
                time.sleep(1)
        except Exception as e:
            print(e)


class StartSensor3(threading.Thread):
    def run(self):
        try:
            print('Sensor 1 Start!')
            for i in range(60):
                acceleration_sensor = Acceleration.objects.create(
                    valueX=random.uniform(-0.09, -0.01),
                    valueY=random.uniform(0.01, 0.09),
                    valueZ=random.uniform(1.01, 1.09),
                    unit=Unit.objects.get(pk=1)
                )
                gyroscope_sensor = Gyroscope.objects.create(
                    valueX=random.uniform(-1.8, -0.2),
                    valueY=random.uniform(12.1, 13),
                    valueZ=random.uniform(12.1, 13),
                    unit=Unit.objects.get(pk=2)
                )
                rotation_sensor = Rotation.objects.create(
                    rotationX=random.uniform(0.9, 16.9),
                    rotationY=random.uniform(0.01, 4.9),
                    rotationZ=random.uniform(-45, 45),
                    unit=Unit.objects.get(pk=3)
                )
                data = {'date': str(datetime.datetime.now()), 'UUID': '68164eba-6d25-4d8b-982b-8f0803d21dff',
                        'Touch': 'no touch detected',
                        'data': [acceleration_sensor.getJson(), gyroscope_sensor.getJson(), rotation_sensor.getJson()]}

                payload_json = json.dumps(data, indent=4)
                headers = {
                    "accept": "text/plain, */*; q=0.01",
                    "accept-language": "en-US,en;q=0.9",
                    "content-type": "application/json; charset=UTF-8"
                }
                url = 'https://livedatawebsocket.herokuapp.com/sensor/post/'

                x = requests.post(url, verify=True, data=payload_json, headers=headers)
                time.sleep(1)
        except Exception as e:
            print(e)

