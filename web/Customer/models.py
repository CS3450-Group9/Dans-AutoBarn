from django.db import models
from UserAuth.models import UserProfile
from Manager.models import Car

class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    confirmed = models.BooleanField()
    processed_on = models.DateTimeField()
    
    def get_num_days(self):
        days = self.end_date.day - self.start_date.day
        return days
    
    def return_date(self):
        days = self.get_num_days()
        return f"Reserved for {days} days from {self.start_date} to {self.end_date}"
    