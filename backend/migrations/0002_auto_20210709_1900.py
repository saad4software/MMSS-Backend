# Generated by Django 3.2 on 2021-07-09 16:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='motivation',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 9, 19, 0, 33, 148579)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 9, 19, 0, 33, 164210)),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='from_date',
            field=models.DateField(verbose_name=datetime.datetime(2021, 7, 9, 19, 0, 33, 148579)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(verbose_name=datetime.datetime(2021, 7, 9, 19, 0, 33, 164210)),
        ),
    ]