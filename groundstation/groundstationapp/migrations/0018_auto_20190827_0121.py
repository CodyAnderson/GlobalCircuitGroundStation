# Generated by Django 2.2.3 on 2019-08-27 01:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groundstationapp', '0017_conductivitymeasurementsunits_measurementsunits_packetv6units'),
    ]

    operations = [
        migrations.AddField(
            model_name='packetv6units',
            name='commands_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='packetv6units',
            name='conductivity_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 27, 1, 21, 20, 170377)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='packetv6units',
            name='mcu_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='packetv6units',
            name='satellites_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='packetv6units',
            name='sequence_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='packetv6units',
            name='version',
            field=models.TextField(null=True),
        ),
    ]
