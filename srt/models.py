from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.conf import settings
# Create your models here.


#  매크로 신청 정보 MASTER: mecro_case
class MecroMaster(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mecro_case')  # User.mecro_case.all() -> 해당 유저가 신청한 매크로 건들
    mecro_id = models.CharField(max_length=200)
    korailID = models.CharField(max_length=50)
    time_in = models.DateTimeField(null=True)
    time_out = models.DateTimeField(null=True)
    dep  = models.CharField(max_length=200)
    arr = models.CharField(max_length=200)
    date  = models.CharField(max_length=200)
    dep_time_from = models.CharField(max_length=200)
    dep_time_to	 = models.CharField(max_length=200)
    first_seat_YN = models.CharField(max_length=10)
    task_ID = models.CharField(max_length=200, default='0000000')
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.mecro_id





