from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# extend provided user class to accomadate our needs
class UserProfile(models.Model):
    # create a subclass to be used as an enum for the type of user
    # https://stackoverflow.com/questions/54802616/how-can-one-use-enums-as-a-choice-field-in-a-django-model
    class UserType(models.TextChoices):
        Customer    = 'CU', _('Customer')
        TillWorker  = 'TW', _('TillWorker')
        CarRetrival = "CR", _('CarRetrievalSpecialist')
        Manager     = 'MA', _('Manager')

    user = models.OneToOneField(User, on_delete=models.CASCADE) # use existing django auth.user
    auth_level = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.Customer,
    )
    balance = models.PositiveIntegerField(default=0)

    def __repr__(self): # For testing purposes
        return "Username:" + self.user.username
    
# these functions tie together the UserProfile model and the default django User profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
