# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#BEGIN OLD MODELS FROM BEFORE PACKET V6
#BEGIN OLD MODELS FROM BEFORE PACKET V6
#BEGIN OLD MODELS FROM BEFORE PACKET V6
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

class Status(models.Model):
  id = models.AutoField(primary_key=True)
  global_id = models.ForeignKey(Packet, on_delete=models.CASCADE)
  yikes = models.IntegerField()
  ballast = models.IntegerField()
  cutdown = models.IntegerField()

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
  sub_id = models.BigIntegerField()
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
#END OLD MODELS FROM BEFORE PACKET V6
#END OLD MODELS FROM BEFORE PACKET V6
#END OLD MODELS FROM BEFORE PACKET V6

class Request(models.Model):
  id = models.AutoField(primary_key=True)
  
  time = models.DateTimeField()
  
  processing_duration = models.DurationField()
  
  forwarded_for_address = models.TextField()
  forwarded_host_address = models.TextField()
  forwarded_server_address = models.TextField()
  remote_address = models.TextField()
  
  raw_request_data = models.TextField()

  response_duration = models.DurationField()
  response_errors = models.TextField()
  response_status_code = models.TextField()
  
class IridiumTransmission(models.Model):
  parent_request = models.OneToOneField(Request, related_name='child_transmission', on_delete=models.CASCADE, primary_key=True)
  
  time = models.DateTimeField()
  
  latitude = models.FloatField()
  longitude = models.FloatField()
  
  cep = models.FloatField()
  momsn = models.IntegerField()
  imei = models.BigIntegerField()
  
  transmitted_via_satellite = models.BooleanField(default=True)
  
class RawPacket(models.Model):
  parent_transmission = models.OneToOneField(IridiumTransmission, related_name='child_raw_packet', on_delete=models.CASCADE, primary_key=True)
  
  data = models.BinaryField()
  hexdata = models.TextField()
  
class PacketV6(models.Model):
  parent_transmission = models.OneToOneField(IridiumTransmission, related_name='child_packet', on_delete=models.CASCADE, primary_key=True)
  
  yikes_status = models.IntegerField()
  
  mcu_id = models.IntegerField()
  version = models.IntegerField()
  
  sequence_id = models.IntegerField()
  
  time = models.DateTimeField()
  
  latitude = models.FloatField()
  longitude = models.FloatField()
  
  altitude = models.FloatField()
  
  ballast_status = models.IntegerField()
  cutdown_status = models.IntegerField()
  
  conductivity_time = models.DateTimeField()
  
  satellites_count = models.IntegerField()
  
  rockblock_signal_strength = models.IntegerField()
  
  commands_count = models.IntegerField()
  
  altimeter_temp = models.IntegerField()
  altimeter_pressure = models.IntegerField()
  
  positive_7v_battery_voltage = models.IntegerField()
  negative_7v_battery_voltage = models.IntegerField()
  
  positive_3v6_battery_voltage = models.IntegerField()
  
  current_draw_7v_rail = models.IntegerField()
  current_draw_3v3_rail = models.IntegerField()
  
  battery_temp = models.IntegerField()
  mcu_temp = models.IntegerField()
  compass_temp = models.IntegerField()
  adc1_temp = models.IntegerField()
  adc2_temp = models.IntegerField()
  external_temp = models.IntegerField()
  rockblock_temp = models.IntegerField()
  
class Measurements(models.Model):
  parent_packet = models.ForeignKey(Packet, on_delete=models.CASCADE)
  
  time = models.DateTimeField()
  
  vert1 = models.IntegerField()
  vert2 = models.IntegerField()
  vertD = models.IntegerField()
  
  compassX = models.IntegerField()
  compassY = models.IntegerField()
  compassZ = models.IntegerField()
  
  horiz1 = models.IntegerField()
  horiz2 = models.IntegerField()
  horizD = models.IntegerField()
  
class ConductivityMeasurements(models.Model):
  parent_packet = models.ForeignKey(Packet, on_delete=models.CASCADE)
  #parent_conductivity_packet = models.ForeignKey(Packet, on_delete=models.CASCADE)
  
  time = models.DateTimeField()
  
  vert1 = models.IntegerField()
  vert2 = models.IntegerField()
  