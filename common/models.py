from django.db import models
from django.contrib.auth.models import AbstractUser



class SrtUser(AbstractUser):
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    korailID = models.CharField(max_length=50, blank=True, null=True)
