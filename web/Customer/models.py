from django.db import models
from UserAuth.models import UserProfile
from Manager.models import Car

class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    
    def get_num_days(self):
        days = self.endDate.day - self.startDate.day
        return days
    
    def return_date(self):
        days = self.get_num_days()
        return f"Reserved for {days} days from {self.startDate} to {self.endDate}"
    