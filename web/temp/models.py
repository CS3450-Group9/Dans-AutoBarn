from django.db import models

# Create your models here.
class Temp(models.Model):
    user_name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)