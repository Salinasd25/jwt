from django.db import models

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

# Create your models here.

class WhiteList_TokenDevice(models.Model):
    ip = models.CharField(max_length=50)
    browser = models.CharField(max_length=255)
    token = models.OneToOneField(OutstandingToken, on_delete=models.CASCADE, related_name='dasdsada')
    created_at = models.DateTimeField(auto_now_add=True)
    
class WhiteListTokenDevice(models.Model):
    ip = models.CharField(max_length=50)
    browser = models.CharField(max_length=255)
    token = models.OneToOneField(OutstandingToken, on_delete=models.CASCADE, related_name='whitelist')
    created_at = models.DateTimeField(auto_now_add=True)