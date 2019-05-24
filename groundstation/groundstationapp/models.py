# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Packet(model.Model):
    id = models.AutoField(primary_key=True)
    packet_id = models.IntegerField()
    version = models.IntegerField()

class IridiumData(model.Model):
    global_id = models.ForeignKey(Packet, on_delete=models.CASCADE)
    transmit_time = models.DateTimeField()
    iridium_latitude = models.FloatField()
    iridium_longitude = models.FloatField()
    iridium_cep = models.FloatField()
    momsn = models.IntegerField()
    imei = models.BigIntegerField()
