from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    # create a subclass to be used as an enum for the type of user
    # https://stackoverflow.com/questions/54802616/how-can-one-use-enums-as-a-choice-field-in-a-django-model
    class UserType(models.TextChoices):
        Customer    = 'CU', _('Customer')
        TillWorker  = 'TW', _('TillWorker')
        CarRetrival = "CR", _('CarRetrievalSpecialist')
        Manager     = 'MA', _('Manager')

    name = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32) # TODO: RESEARCH: how do we hash this
    type = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.Customer,
    )
    balance = models.IntegerField(default=0)
    