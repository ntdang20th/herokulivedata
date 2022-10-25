import datetime

from django.shortcuts import render
from .thread import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import mail

connection = mail.get_connection()



async def home_sensor(request):
    return render(request, 'home_sensor.html')

def home(request):
    return render(request, 'home.html')


def generate_sensor_data(request):
    total = request.GET.get('total')
    CreateSensorThread(int(total)).start()
    return JsonResponse({'status': 200})

def generate_sensor1(request):
    StartSensor1().start()
    return JsonResponse({'status': 200})

def generate_sensor2(request):
    StartSensor2().start()
    return JsonResponse({'status': 200})

def generate_sensor3(request):
    StartSensor3().start()
    return JsonResponse({'status': 200})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def ResponesData(request):
    data = request.data
    print(data)
    current_time = data['date']

    try:
        device = Device.objects.get(uuid=data['UUID'])
    except Device.DoesNotExist:
        device = Device.objects.create(uuid=data['UUID'], description='unknown device')

    try:
        touch = TouchStatus.objects.get(status_name=data['Touch'])
    except TouchStatus.NotExists:
        touch = TouchStatus.objects.create(status_name=data['Touch'], description='unknown device')

    acceleration = data['data'][0]
    gyroscope = data['data'][1]
    rotation = data['data'][2]

    acceleration_sensor = Acceleration.objects.create(
        valueX=acceleration['valueX'],
        valueY=acceleration['valueY'],
        valueZ=acceleration['valueZ'],
        unit=Unit.objects.get(pk=1)
    )
    gyroscope_sensor = Gyroscope.objects.create(
        valueX=gyroscope['valueX'],
        valueY=gyroscope['valueY'],
        valueZ=gyroscope['valueZ'],
        unit=Unit.objects.get(pk=2)
    )
    rotation_sensor = Rotation.objects.create(
        rotationX=rotation['RotationX'],
        rotationY=rotation['RotationY'],
        rotationZ=rotation['RotationZ'],
        unit=Unit.objects.get(pk=3)
    )

    #create new rawdata
    try:
        date = datetime.datetime.strptime(current_time, 'YYYY-MM-DD HH:MM:ss')
    except ValueError as err:
        date = datetime.datetime.now()
        print(err)

    print(date)

    rawdata = Rawdata.objects.create(
        date=date,
        device=device,
        touch_status=touch,
        acceleration=acceleration_sensor,
        gyroscope=gyroscope_sensor,
        rotation=rotation_sensor
    )


    # connection.open()
    # send_mail(
    #     'Reply mess!!',
    #     json_string,
    #     settings.EMAIL_HOST_USER,
    #     ['ntdang_20th@student.agu.edu.vn', 'eliane.schroeter@gmail.com'],
    #     connection=connection,
    # )
    # connection.close()
    return Response(request.data)

