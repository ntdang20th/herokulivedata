from django.urls import path
from .views import *

urlpatterns = [
    path('', home_sensor),
    path('test', home),
    path('post/', ResponesData),
    path('simulate-sensors/', generate_sensor_data),
    path('start-sensor1/', generate_sensor1),
    path('start-sensor2/', generate_sensor2),
    path('start-sensor3/', generate_sensor3),
]