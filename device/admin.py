from django.contrib import admin
from .models import *

admin.site.register(Unit)
admin.site.register(Acceleration)
admin.site.register(Gyroscope)
admin.site.register(Rotation)
admin.site.register(TouchStatus)
admin.site.register(Rawdata)