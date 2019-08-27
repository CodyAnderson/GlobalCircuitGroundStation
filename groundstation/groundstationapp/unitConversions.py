#vert1,2,D , horiz1,2,D (V)
def adc_conv(sig):
  return sig*3.3/1023.0

#altimeter_temp (°C)
def altimeter_temp_conv_C(sig):
  return (sig/100)-273.15

#altimeter_temp (°K)
def altimeter_temp_conv_K(sig):
  return sig/100

#altimeter_pressure (mBars)
def altimeter_pressure_conv(sig):
  return sig/100

#positive_7v_battery_voltage (V)
def positive_7v_battery_voltage_conv(sig):
  return sig*3.3/1023.0*3.004
  
#negative_7v_battery_voltage (V)
def negative_7v_battery_voltage_conv(sig):
  return sig*3.3/1023.0*(-3.25)
  
#positive_3v6_battery_voltage (V)
def positive_3v6_battery_voltage_conv(sig):
  return sig*3.3/1023.0*5.0/3.0
  
#current_draw_7v_rail (mA)
def current_draw_7v_rail_conv(sig):
  return sig*3.3/1023.0*51.0
  
#current_draw_3v3_rail (mA)
def current_draw_3v3_rail_conv(sig):
  return sig*3.3/1023.0*500.0
  
#battery_temp, mcu_temp (°C)
def backplane_temp_conv_C(sig):
  return (sig*3.3/1023.0*111.0)-273.15
  
#battery_temp, mcu_temp (°K)
def backplane_temp_conv_K(sig):
  return sig*3.3/1023.0*111.0
  
#compass_temp (°C)
def compass_temp_conv_C(sig):
  return sig+10.0
  
#compass_temp (°K)
def compass_temp_conv_K(sig):
  return sig+283.15
  
#adc1_temp, adc2_temp (°C)
def adc_temp_conv_C(sig):
  return sig*0.03125

#adc1_temp, adc2_temp (°K)
def adc_temp_conv_K(sig):
  return (sig*0.03125)+273.15
  
#external_temp, rockblock_temp (°C)
def harness_temp_conv_C(sig):
  return ((sig*3.3/1023.0)-2.4)*100

#external_temp, rockblock_temp (°K)
def harness_temp_conv_K(sig):
  return (((sig*3.3/1023.0)-2.4)*100)+273.15

#altitude (m)
def altitude_temp_conv(sig):
  return sig/10.0

#yikes_status  
def yikes_status_conv(sig):
  message = ""
  if(sig&0b1):
    message = message + "System reset, "
  if(sig&0b10):
    message = message + "Tick took more than 100ms to complete, "
  if(sig&0b100):
    message = message + "GPS PPS early/late/missing, "
  if(sig&0b1000):
    message = message + "RockBLOCK error, "
  if(sig&0b10000):
    message = message + "RockBLOCK response timed out, "
  if(sig&0b100000):
    message = message + "GPS signal not locked, "
  if(sig&0b1000000):
    message = message + "Conductivity polarity: -V1/+V2"
  else
    message = message + "Conductivity polarity: +V1/-V2"
  return message
  
#ballast status
def ballast_status_conv(sig):
  if(sig==0x00):
    return "Idle"
  else if(sig==0x01):
    return "Successfully dropped"
  else if(sig==0x02):
    return "Failed to address"
  else if(sig==0x03):
    return "Failed to arm"
  else if(sig==0x04):
    return "Failed to fire"
  else if(sig==0xAC):
    return "Request acknowledged; Send confirmation"
    
#cutdown_status
def cutdown_status_conv(sig):
  if(sig==0x00):
    return "Idle"
  else if(sig==0x01):
    return "Successfully cut down"
  else if(sig==0x02):
    return "XBee communication in progress"
  else if(sig==0x03):
    return "PIC16 error"
  else if(sig==0x04):
    return "XBee communication failure"
  else if(sig==0x05):
    return "Failure message recieved from cutdown module"
  else if(sig==0xAC):
    return "Request acknowledged; Send confirmation"