from django.db import models
from django.utils import timezone
from UserAuth.models import User
from Manager.models import Car

# Create your models here.

class Reservation(models.Model):
    # car = models.ForeignKey(Car, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    renterID = models.CharField(max_length=50)
    renterName = models.CharField(max_length=50)
    plateNumber = models.CharField(max_length=50)
    
    # def createReservation():
    #     reservation = Reservation()
    
    # def cancelReservation():
    #     pass