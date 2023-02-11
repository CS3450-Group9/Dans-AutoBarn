from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


# reference to information about how this user model is setup
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-user
class UserProfile(models.Model):
    # create a subclass to be used as an enum for the type of user
    # https://stackoverflow.com/questions/54802616/how-can-one-use-enums-as-a-choice-field-in-a-django-model
    class UserType(models.TextChoices):
        Customer    = 'CU', _('Customer')
        TillWorker  = 'TW', _('TillWorker')
        CarRetrival = "CR", _('CarRetrievalSpecialist')
        Manager     = 'MA', _('Manager')

    user = models.OneToOneField(User, on_delete=models.CASCADE) # use existing django auth.user
    authLevel = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.Customer,
    )
    balance = models.IntegerField(default=0)
    