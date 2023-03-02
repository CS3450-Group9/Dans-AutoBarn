# Generated by Django 4.1 on 2023-02-25 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('renterID', models.CharField(max_length=50)),
                ('renterName', models.CharField(max_length=50)),
                ('plateNumber', models.CharField(max_length=10)),
            ],
        ),
    ]
