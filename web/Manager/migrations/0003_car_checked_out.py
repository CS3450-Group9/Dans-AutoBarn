# Generated by Django 4.1 on 2023-04-05 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0002_populate'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='checked_out',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 4.1.2 on 2023-04-05 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0002_populate'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='checked_out',
            field=models.BooleanField(default=False),
        ),
    ]
