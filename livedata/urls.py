from django.urls import path
from .views import *

urlpatterns = [
    path('', home_sensor),
    path('post/', ResponesData),
    path('simulate-sensors/', generate_sensor_data),
]