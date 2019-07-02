# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class IridiumData(models.Model):
		id = models.AutoField(primary_key=True)
		transmit_time = models.DateTimeField()
		iridium_latitude = models.FloatField()
		iridium_longitude = models.FloatField()
		iridium_cep = models.FloatField()
		momsn = models.IntegerField()
		imei = models.BigIntegerField()
		transmitted_via_satellite = models.BooleanField(default=True)

class Packet(models.Model):
		id = models.AutoField(primary_key=True)
		global_id = models.ForeignKey(IridiumData, on_delete=models.CASCADE)
		packet_id = models.IntegerField(null=True)
		version = models.IntegerField(null=True)



class SlowMeasurement(models.Model):
		id = models.AutoField(primary_key=True)
		global_id = models.ForeignKey(Packet, on_delete=models.CASCADE)
		gps_latitude = models.FloatField()
		gps_longitude = models.FloatField()
		gps_altitude = models.FloatField()
		gps_time = models.DateTimeField()
		cond_gps_time = models.DateTimeField()

class RawData(models.Model):
		global_id = models.ForeignKey(Packet, on_delete=models.CASCADE)
		data = models.BinaryField()
		hexdata = models.TextField()

class SupData(models.Model):
		global_id = models.ForeignKey(Packet, on_delete=models.CASCADE)
		sub_id = models.IntegerField()
		type = models.TextField()
		value = models.IntegerField()

class ConductivityData(models.Model):
		global_id = models.ForeignKey(SlowMeasurement, on_delete=models.CASCADE)
		sub_id = models.IntegerField()
		vert1 = models.IntegerField()
		vert2 = models.IntegerField()

class FastMeasurement(models.Model):
		global_id = models.ForeignKey(Packet, on_delete=models.CASCADE)
		sub_id = models.IntegerField()
		vert1 = models.IntegerField()
		vert2 = models.IntegerField()
		vertD = models.IntegerField()
		compassX = models.IntegerField()
		compassY = models.IntegerField()
		compassZ = models.IntegerField()
		horiz1 = models.IntegerField()
		horiz2 = models.IntegerField()
		horizD = models.IntegerField()
