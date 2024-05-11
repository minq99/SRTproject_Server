from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CustomUser(User):
    phone_number = models.CharField(max_length=15, blank=True, null=True)