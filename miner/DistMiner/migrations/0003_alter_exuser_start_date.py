# Generated by Django 3.2.6 on 2021-08-10 01:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('DistMiner', '0002_exuser_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exuser',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 10, 1, 19, 41, 60010, tzinfo=utc)),
        ),
    ]