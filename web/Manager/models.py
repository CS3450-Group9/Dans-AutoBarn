from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    gasFillPercent = models.IntegerField()
    plateNumber = models.CharField(max_length=50)
    photoID = models.CharField(max_length=50)
    lowjacked = models.BooleanField(default=False)