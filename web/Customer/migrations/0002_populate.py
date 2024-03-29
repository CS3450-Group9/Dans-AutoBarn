# Generated by Django 4.1 on 2023-03-11 23:57

from django.db import migrations
from django.utils import timezone


def populate_db(apps, schema_editor):
    
    start_date = '2025-01-01'
    end_date = '2025-01-05'
    
    Reservation = apps.get_model('Customer', 'Reservation')
    Car = apps.get_model('Manager', 'Car')
    UserProfile = apps.get_model('UserAuth', 'UserProfile')
    
    car1 = Car.objects.get(pk=1)
    car2 = Car.objects.get(pk=2)
    car8 = Car.objects.get(pk=8)
    
    new_admin = UserProfile.objects.get(pk=1)
    new_customer = UserProfile.objects.get(pk=2)
    
    res1 = Reservation(car=car1, user=new_admin, start_date=start_date, end_date=end_date, confirmed=True, processed_on=timezone.now())
    res2 = Reservation(car=car2, user=new_customer, start_date=start_date, end_date=end_date, confirmed=True, processed_on=timezone.now())
    res21 = Reservation(car=car8, user=new_admin, start_date='2023-03-28', end_date='2023-03-31', confirmed=True, processed_on=timezone.now())
    res3 = Reservation(car=car8, user=new_admin, start_date='2023-04-01', end_date='2023-04-05', confirmed=True, processed_on=timezone.now())
    res4 = Reservation(car=car8, user=new_admin, start_date='2023-04-06', end_date='2023-04-10', confirmed=True, processed_on=timezone.now())
    res1.save()
    res2.save()
    res21.save()
    res3.save()
    res4.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db),
    ]
