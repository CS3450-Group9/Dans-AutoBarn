from django.db import models
from UserAuth.models import User
from Manager.models import Car

# Create your models here.

class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    
    def get_num_days(self):
        days = self.endDate.day - self.startDate.day
        return days
    
    def return_date(self):
        days = self.get_num_days()
        return f"Reserved for {days} days from {self.startDate} to {self.endDate}"
    