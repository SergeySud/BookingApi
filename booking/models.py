from django.contrib.auth.models import User
from django.db import models

from accounts.models import CustomUser


# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=3)
    guests_number = models.IntegerField()


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reservation_start_date = models.DateField()
    reservation_end_date = models.DateField()
    reserved_by_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
