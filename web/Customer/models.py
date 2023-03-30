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
        days = self.end_date - self.start_date
        return days.days + 1

    def get_total_cost(self):
        return self.car.reservation_cost * self.get_num_days()
    