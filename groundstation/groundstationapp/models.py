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
  
  processing_duration = models.DurationField(null=True)
  
  forwarded_for_address = models.TextField()
  forwarded_host_address = models.TextField()
  forwarded_server_address = models.TextField()
  remote_address = models.TextField()
  
  raw_request_data = models.TextField(null=True)

  response_duration = models.DurationField(null=True)
  response_errors = models.TextField(null=True)
  response_status_code = models.TextField(null=True)
  
  
class IridiumTransmission(models.Model):
  parent_request = models.OneToOneField(Request, related_name='child_transmission', on_delete=models.CASCADE, primary_key=True)
  
  time = models.DateTimeField()
  
  latitude = models.FloatField()
  longitude = models.FloatField()
  
  cep = models.FloatField()
  momsn = models.IntegerField()
  imei = models.BigIntegerField()
  
  device_type = models.TextField(null=True)
  serial = models.IntegerField(null=True)
  iridium_session_status = models.TextField(null=True)
  
  transmitted_via_satellite = models.BooleanField(default=True)
  
  
class RawPacket(models.Model):
  parent_transmission = models.OneToOneField(IridiumTransmission, related_name='child_raw_packet', on_delete=models.CASCADE, primary_key=True)
  
  data = models.BinaryField(null=True)
  hexdata = models.TextField(null=True)
  
  
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
  altimeter_pressure = models.BigIntegerField()
  
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
  
class PacketV6Units(models.Model):
  parent_packet_v6 = models.OneToOneField(PacketV6, related_name='child_packet_v6_units', on_delete=models.CASCADE, primary_key=True)
  
  yikes_status = models.TextField(null=True)
  mcu_id = models.TextField(null=True)
  
  version = models.TextField(null=True)
  sequence_id = models.TextField(null=True)
  
  time = models.DateTimeField()
  
  latitude = models.FloatField()
  longitude = models.FloatField()
  altitude = models.FloatField()
  
  ballast_status = models.TextField(null=True)
  cutdown_status = models.TextField(null=True)
  
  conductivity_time = models.DateTimeField()
  satellites_count = models.IntegerField()
  rockblock_signal_strength = models.FloatField()
  
  commands_count = models.IntegerField()

  altimeter_temp = models.FloatField()
  altimeter_pressure = models.FloatField()
  
  positive_7v_battery_voltage = models.FloatField()
  negative_7v_battery_voltage = models.FloatField()
  
  positive_3v6_battery_voltage = models.FloatField()
  
  current_draw_7v_rail = models.FloatField()
  current_draw_3v3_rail = models.FloatField()
  
  battery_temp = models.FloatField()
  mcu_temp = models.FloatField()
  compass_temp = models.FloatField()
  adc1_temp = models.FloatField()
  adc2_temp = models.FloatField()
  external_temp = models.FloatField()
  rockblock_temp = models.FloatField()
  
  
class Measurements(models.Model):
  parent_packet = models.ForeignKey(PacketV6, on_delete=models.CASCADE)
  
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
  
class MeasurementsUnits(models.Model):
  parent_measurements = models.OneToOneField(Measurements, related_name='child_measurements_units', on_delete=models.CASCADE, primary_key=True)
  
  time = models.DateTimeField()
  
  vert1 = models.FloatField()
  vert2 = models.FloatField()
  vertD = models.FloatField()
  
  compassX = models.FloatField()
  compassY = models.FloatField()
  compassZ = models.FloatField()
  
  horiz1 = models.FloatField()
  horiz2 = models.FloatField()
  horizD = models.FloatField()


class ConductivityMeasurements(models.Model):
  parent_packet = models.ForeignKey(PacketV6, on_delete=models.CASCADE)
  #parent_conductivity_packet = models.ForeignKey(Packet, on_delete=models.CASCADE)
  
  time = models.DateTimeField()
  
  vert1 = models.IntegerField()
  vert2 = models.IntegerField()
  
class ConductivityMeasurementsUnits(models.Model):
  parent_conductivity_measurements = models.OneToOneField(ConductivityMeasurements, related_name='child_conductivity_measurements_units', on_delete=models.CASCADE, primary_key=True)
  
  time = models.DateTimeField()
  
  vert1 = models.FloatField()
  vert2 = models.FloatField()
  