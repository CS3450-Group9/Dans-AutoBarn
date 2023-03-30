from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from Customer.models import Reservation

@receiver(user_logged_out)
def delete_unconfirmed(sender, user, request, **kwargs):
    '''Deletes user's unconfirmed reservations upon logout'''
    unconfirmed = Reservation.objects.filter(user=user.userprofile, confirmed=False)
    unconfirmed.delete()

user_logged_out.connect(delete_unconfirmed)
