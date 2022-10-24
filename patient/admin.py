from django.contrib import admin
from .models import *

admin.site.register(Device)
admin.site.register(Familiar)
admin.site.register(PatientInfo)
admin.site.register(Patient)
admin.site.register(HasPatientFamiliar)
