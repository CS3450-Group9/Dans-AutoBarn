from django.db import models
from UserAuth.models import UserProfile
from Manager.models import Car

class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    renterID = models.CharField(max_length=50)
    
    class Meta:
        abstract = True
    
    def return_date(self):
        return f"{self.startDate} - {self.endDate}"
    
    # def createReservation():
    #     reservation = Reservation()
    
    # def cancelReservation():
    #     pass