from django.db import models
from core import settings
from address.models import ShareAddress

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    share_address = models.ForeignKey(ShareAddress, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=255, blank=True, null=True)