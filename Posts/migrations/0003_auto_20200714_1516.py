# Generated by Django 3.0.7 on 2020-07-14 14:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0002_auto_20200710_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateField(default=datetime.date(2020, 7, 14)),
        ),
    ]
