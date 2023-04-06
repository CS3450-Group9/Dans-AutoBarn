from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    gas_fill_percent = models.IntegerField()
    plate_number = models.CharField(max_length=50)
    image = models.ImageField(upload_to="cars")
    lowjacked = models.BooleanField(default=False)
    reservation_cost = models.IntegerField()
    checked_out = models.BooleanField(default=False)
    location = models.CharField(max_length=150, default="")
