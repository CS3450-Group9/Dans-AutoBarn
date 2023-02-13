# Generated by Django 4.1.2 on 2023-02-13 03:30

from django.db import migrations

def populate_db(apps, schema_editor):

    UserProfile = apps.get_model('UserAuth', 'UserProfile')
    User = apps.get_model('auth', 'User')

    user1 = User.objects.create_user(username="admin", email="admin@example.com", password="password", is_staff=True)
    user2 = User.objects.create_user(username="customer", email="example@gmail.com", password="hello")
    user3 = User.objects.create_user(username="carperson", email="carperson@gmail.com", password="password", is_staff=True)
    user4 = User.objects.create_user(username="Tillperson", email="tillperson@gmail.com", password="password", is_staff=True)
    new_admin = UserProfile(user=user1, auth_level="MA", balance=999)
    new_customer = UserProfile(user=user2, auth_level="CU", balance=1)
    new_carperson = UserProfile(user=user3, auth_level="CR")
    new_till = UserProfile(user=user4, auth_level="TW", balance=32436)
    new_admin.save()
    new_customer.save()
    new_carperson.save()
    new_till.save()

class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db),
    ]
