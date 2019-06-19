# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-13 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groundstationapp', '0007_auto_20190525_0006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iridiumdata',
            name='global_id',
        ),
        migrations.AddField(
            model_name='iridiumdata',
            name='transmitted_via_satellite',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='packet',
            name='global_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='groundstationapp.IridiumData'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='iridiumdata',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]