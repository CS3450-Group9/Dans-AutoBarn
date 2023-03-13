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
    _auth_level = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.Customer,
        db_column="auth_level"
    )
    _balance = models.IntegerField(default=0, db_column="balance")

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_bal):
        if new_bal < 0:
            raise ValueError
        self._balance = new_bal

    @property
    def auth_level(self):
        return self._auth_level

    @auth_level.setter
    def auth_level(self, new_auth):
        if new_auth not in self.UserType.choices:
            raise ValueError
        self._auth_level = new_auth

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
