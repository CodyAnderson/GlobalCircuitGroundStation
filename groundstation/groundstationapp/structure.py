import struct

PACKET_VERSION=3
def unpack(f):
    values={}
    values['version']=struct.unpack('<B',f.read(1))[0]
    values['yikes']=struct.unpack('<B',f.read(1))[0]
    values['seq']=struct.unpack('<H',f.read(2))[0]
    values['time']=struct.unpack('<I',f.read(4))[0]
    values['lat']=struct.unpack('<I',f.read(4))[0]
    values['lon']=struct.unpack('<I',f.read(4))[0]
    values['alt']=struct.unpack('<I',f.read(4))[0]
    values['horiz1']=struct.unpack('<12H',f.read(24))
    values['horiz2']=struct.unpack('<12H',f.read(24))
    values['horizD']=struct.unpack('<12H',f.read(24))
    values['vert1']=struct.unpack('<12H',f.read(24))
    values['vert2']=struct.unpack('<12H',f.read(24))
    values['vertD']=struct.unpack('<12H',f.read(24))
    values['compassX']=struct.unpack('<12H',f.read(24))
    values['compassY']=struct.unpack('<12H',f.read(24))
    values['compassZ']=struct.unpack('<12H',f.read(24))
    values['cVert1']=struct.unpack('<15H',f.read(30))
    values['cVert2']=struct.unpack('<15H',f.read(30))
    values['sup']=struct.unpack('<4B',f.read(4))
    return values
  
def unpack_old_new(fstring):
    values={}
    values['version']=struct.unpack('<B',fstring[0:1])[0]
    values['yikes']=struct.unpack('<B',fstring[1:2])[0]
    values['seq']=struct.unpack('<H',fstring[2:4])[0]
    values['time']=struct.unpack('<I',fstring[4:8])[0]
    values['lat']=struct.unpack('<I',fstring[8:12])[0]
    values['lon']=struct.unpack('<I',fstring[12:16])[0]
    values['alt']=struct.unpack('<I',fstring[16:20])[0]
    values['horiz1']=struct.unpack('<12h',fstring[20:44])
    values['horiz2']=struct.unpack('<12h',fstring[44:68])
    values['horizD']=struct.unpack('<12h',fstring[68:92])
    values['vert1']=struct.unpack('<12h',fstring[92:116])
    values['vert2']=struct.unpack('<12h',fstring[116:140])
    values['vertD']=struct.unpack('<12h',fstring[140:164])
    values['compassX']=struct.unpack('<12h',fstring[164:188])
    values['compassY']=struct.unpack('<12h',fstring[188:212])
    values['compassZ']=struct.unpack('<12h',fstring[212:236])
    values['cVert1']=struct.unpack('<15h',fstring[236:266])
    values['cVert2']=struct.unpack('<15h',fstring[266:296])
    values['sup']=struct.unpack('<2H',fstring[296:300])
    values['ballast']=struct.unpack('<B',fstring[300:301])[0]
    values['cutdown']=struct.unpack('<B',fstring[301:302])[0]
    values['cond_time']=struct.unpack('<I',fstring[302:306])[0]

    return values
  ##UNSIGNED
    ## 1 BYTE = '<B'
    ## 2 BYTES = '<H'
    ##
    ## 4 BYTES = '<I'
  ##SIGNED
    ##
    ## 2 BYTES = '<h'
    ##
    ##
def unpack_new(fstring):
  values={}
  values['version']=struct.unpack('<B',fstring[0:1])[0]
  values['yikes']=struct.unpack('<B',fstring[1:2])[0]
  values['seq']=struct.unpack('<H',fstring[2:4])[0]
  try:
    values['time']=struct.unpack('<I',fstring[4:8])[0]
    values['lat']=struct.unpack('<I',fstring[8:12])[0]
    values['lon']=struct.unpack('<I',fstring[12:16])[0]
    values['alt']=struct.unpack('<I',fstring[16:20])[0]
    values['horiz1']=struct.unpack('<12h',fstring[20:44])
    values['horiz2']=struct.unpack('<12h',fstring[44:68])
    values['horizD']=struct.unpack('<12h',fstring[68:92])
    values['vert1']=struct.unpack('<12h',fstring[92:116])
    values['vert2']=struct.unpack('<12h',fstring[116:140])
    values['vertD']=struct.unpack('<12h',fstring[140:164])
    values['compassX']=struct.unpack('<12h',fstring[164:188])
    values['compassY']=struct.unpack('<12h',fstring[188:212])
    values['compassZ']=struct.unpack('<12h',fstring[212:236])
    values['cVert1']=struct.unpack('<15h',fstring[236:266])
    values['cVert2']=struct.unpack('<15h',fstring[266:296])
    #values['sup']=struct.unpack('<2H',fstring[296:300])
    #values['ballast']=struct.unpack('<B',fstring[300:301])[0]
    #values['cutdown']=struct.unpack('<B',fstring[301:302])[0]
    #values['cond_time']=struct.unpack('<I',fstring[302:306])[0]
    values['ballast']=struct.unpack('<B',fstring[296:297])[0]
    values['cutdown']=struct.unpack('<B',fstring[297:298])[0]
    values['cond_time']=struct.unpack('<I',fstring[298:302])[0]
    
    ###BAD BAD NOT GOOD
    ###BAD BAD NOT GOOD
    ###values['sup'] = [0]*20
    ###BAD BAD NOT GOOD
    ###BAD BAD NOT GOOD
    values['sup'] = {}
    values['sup']['GPSSats']=struct.unpack('<B',fstring[302:303])[0]
    values['sup']['RBSig']=struct.unpack('<B',fstring[303:304])[0]
    values['sup']['Commands']=struct.unpack('<B',fstring[304:305])[0]
    values['sup']['AltTemp']=struct.unpack('<I',fstring[305:309])[0]
    values['sup']['AltPress']=struct.unpack('<I',fstring[309:313])[0]
    values['sup']['VbatPlus']=struct.unpack('<H',fstring[313:315])[0]
    values['sup']['VbatMinus']=struct.unpack('<H',fstring[315:317])[0]
    values['sup']['3V6batV']=struct.unpack('<H',fstring[317:319])[0]
    values['sup']['7V_I']=struct.unpack('<H',fstring[319:321])[0]
    values['sup']['3V3_I']=struct.unpack('<H',fstring[321:323])[0]
    values['sup']['Tbat']=struct.unpack('<H',fstring[323:325])[0]
    values['sup']['Tcomp']=struct.unpack('<H',fstring[325:327])[0]
    values['sup']['Tmag']=struct.unpack('<h',fstring[327:329])[0]
    values['sup']['Tadc1']=struct.unpack('<h',fstring[329:331])[0]
    values['sup']['Tadc2']=struct.unpack('<h',fstring[331:333])[0]
    values['sup']['Text']=struct.unpack('<H',fstring[333:335])[0]
    values['sup']['Trock']=struct.unpack('<H',fstring[335:337])[0]
  except Exception as err:
    print("\n\nTHERE WAS AN ERROR READING IN THE PACKET")
    print(str(err) + "\n\n")
  return values
  
def unpackV6(fstring):
  values={}
###PACKET
  #yikes_status = models.IntegerField()
  #mcu_id = models.IntegerField()
  #version = models.IntegerField()
  #sequence_id = models.IntegerField()
  #time = models.DateTimeField()
  #latitude = models.FloatField()
  #longitude = models.FloatField()
  #altitude = models.FloatField()
  #ballast_status = models.IntegerField()
  #cutdown_status = models.IntegerField()
  #conductivity_time = models.DateTimeField()
  #satellites_count = models.IntegerField()
  #rockblock_signal_strength = models.IntegerField()
  #commands_count = models.IntegerField()
  #altimeter_temp = models.IntegerField()
  #altimeter_pressure = models.IntegerField()
  #positive_7v_battery_voltage = models.IntegerField()
  #negative_7v_battery_voltage = models.IntegerField()
  #positive_3v6_battery_voltage = models.IntegerField()
  #current_draw_7v_rail = models.IntegerField()
  #current_draw_3v3_rail = models.IntegerField()
  #battery_temp = models.IntegerField()
  #mcu_temp = models.IntegerField()
  #compass_temp = models.IntegerField()
  #adc1_temp = models.IntegerField()
  #adc2_temp = models.IntegerField()
  #external_temp = models.IntegerField()
  #rockblock_temp = models.IntegerField()
###MEASUREMENT
  #vert1 = models.IntegerField()
  #vert2 = models.IntegerField()
  #vertD = models.IntegerField()
  #compassX = models.IntegerField()
  #compassY = models.IntegerField()
  #compassZ = models.IntegerField()
  #horiz1 = models.IntegerField()
  #horiz2 = models.IntegerField()
  #horizD = models.IntegerField()
###CONDUCTIVITY MEASUREMENT
  #vert1 = models.IntegerField()
  #vert2 = models.IntegerField()
  
  print(fstring)
  
  
  tempVersion=struct.unpack('<B',fstring[0:1])[0]
  values['version'] = tempVersion & 0b00001111
  values['mcu_id'] = (tempVersion & 0b11110000) >> 4
  values['yikes_status']=struct.unpack('<B',fstring[1:2])[0]
  values['sequence_id']=struct.unpack('<H',fstring[2:4])[0]
  try:
    values['time']=struct.unpack('<I',fstring[4:8])[0]
    values['latitude']=struct.unpack('<I',fstring[8:12])[0]
    values['longitude']=struct.unpack('<I',fstring[12:16])[0]
    values['altitude']=struct.unpack('<I',fstring[16:20])[0]
    values['horiz1']=struct.unpack('<12h',fstring[20:44])
    values['horiz2']=struct.unpack('<12h',fstring[44:68])
    values['horizD']=struct.unpack('<12h',fstring[68:92])
    values['vert1']=struct.unpack('<12h',fstring[92:116])
    values['vert2']=struct.unpack('<12h',fstring[116:140])
    values['vertD']=struct.unpack('<12h',fstring[140:164])
    values['compassX']=struct.unpack('<12h',fstring[164:188])
    values['compassY']=struct.unpack('<12h',fstring[188:212])
    values['compassZ']=struct.unpack('<12h',fstring[212:236])
    values['conductivity_vert1']=struct.unpack('<15h',fstring[236:266])
    values['conductivity_vert2']=struct.unpack('<15h',fstring[266:296])
    values['ballast_status']=struct.unpack('<B',fstring[296:297])[0]
    values['cutdown_status']=struct.unpack('<B',fstring[297:298])[0]
    values['conductivity_time']=struct.unpack('<I',fstring[298:302])[0]
    values['satellites_count']=struct.unpack('<B',fstring[302:303])[0]
    values['rockblock_signal_strength']=struct.unpack('<B',fstring[303:304])[0]
    values['commands_count']=struct.unpack('<B',fstring[304:305])[0]
    values['altimeter_temp']=struct.unpack('<I',fstring[305:309])[0]
    values['altimeter_pressure']=struct.unpack('<I',fstring[309:313])[0]
    values['positive_7v_battery_voltage']=struct.unpack('<H',fstring[313:315])[0]
    values['negative_7v_battery_voltage']=struct.unpack('<H',fstring[315:317])[0]
    values['positive_3v6_battery_voltage']=struct.unpack('<H',fstring[317:319])[0]
    values['current_draw_7v_rail']=struct.unpack('<H',fstring[319:321])[0]
    values['current_draw_3v3_rail']=struct.unpack('<H',fstring[321:323])[0]
    values['battery_temp']=struct.unpack('<H',fstring[323:325])[0]
    values['mcu_temp']=struct.unpack('<H',fstring[325:327])[0]
    values['compass_temp']=struct.unpack('<h',fstring[327:329])[0]
    values['adc1_temp']=struct.unpack('<h',fstring[329:331])[0]
    values['adc2_temp']=struct.unpack('<h',fstring[331:333])[0]
    values['external_temp']=struct.unpack('<H',fstring[333:335])[0]
    values['rockblock_temp']=struct.unpack('<H',fstring[335:337])[0]
  except Exception as err:
    print("\n\nTHERE WAS AN ERROR READING IN THE V6 PACKET")
    print(str(err) + "\n\n")
  return values
