from django.shortcuts import render

from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from graphos.renderers.gchart import LineChart

from . import models
from .imeiNames import imeiNames
import super_secrets as secrets

import datetime as dt
from datetime import datetime
from datetime import timedelta

from .graphs.conductivity import conductivity
from .graphs.horizontal   import horizontal
from .graphs.vertical    import vertical
from .graphs.compass     import compass
from .graphs.cep       import cep
from .graphs.gps       import gps
from .graphs.gpsAltitude       import gpsAltitude
from .graphs.iridium       import iridium
from .graphs.termStatus import termStatus
from .graphs.supervision import supervision
from .graphs.supervisionPressure import supervisionPressure
from .graphs.supervisionTemp import supervisionTemp

signalFunctions = {
  'conductivity': conductivity,
  'horizontal'  : horizontal,
  'vertical'     : vertical,
  'compass'    : compass,
  'cep'      : cep,
  'gps'      : gps,
  'gpsAltitude' : gpsAltitude,
  'iridium'      : iridium,
  'termStatus': termStatus,
  'supervision': supervision,
  'supervisionPressure': supervisionPressure,
  'supervisionTemp': supervisionTemp,
  }
  
functionsList = [
  ['Request',
    [
      'time',
      'processing_duration',
      'forwarded_for_address',
      'forwarded_host_address',
      'forwarded_server_address',
      'remote_address',
      'raw_request_data',
      'response_duration',
      'response_errors',
      'response_status_code',
    ]
  ],
  ['IridiumTransmission',
    [
      'time',
      'latitude',
      'longitude',
      'cep',
      'momsn',
      'imei',
      'device_type',
      'serial',
      'iridium_session_status',
      'transmitted_via_satellite'
    ]
  ],
  ['RawPacket',
    [
      'hexdata',
    ]
  ],
  ['PacketV6',
    [
      'time',
      'yikes_status',
      'mcu_id',
      'version',
      'sequence_id',
      'latitude',
      'longitude',
      'altitude',
      'ballast_status',
      'cutdown_status',
      'conductivity_time',
      'satellites_count',
      'rockblock_signal_strength',
      'commands_count',
      'altimeter_temp',
      'altimeter_pressure',
      'positive_7v_battery_voltage',
      'negative_7v_battery_voltage',
      'positive_3v6_battery_voltage',
      'current_draw_7v_rail',
      'current_draw_3v3_rail',
      'battery_temp',
      'mcu_temp',
      'compass_temp',
      'adc1_temp',
      'adc2_temp',
      'external_temp',
      'rockblock_temp',
    ]
  ],
  ['PacketV6Units',
    [
      'time',
      'yikes_status',
      'mcu_id',
      'version',
      'sequence_id',
      'latitude',
      'longitude',
      'altitude',
      'ballast_status',
      'cutdown_status',
      'conductivity_time',
      'satellites_count',
      'rockblock_signal_strength',
      'commands_count',
      'altimeter_temp',
      'altimeter_pressure',
      'positive_7v_battery_voltage',
      'negative_7v_battery_voltage',
      'positive_3v6_battery_voltage',
      'current_draw_7v_rail',
      'current_draw_3v3_rail',
      'battery_temp',
      'mcu_temp',
      'compass_temp',
      'adc1_temp',
      'adc2_temp',
      'external_temp',
      'rockblock_temp',
    ]
  ],
  ['Measurements',
    [
      'time',
      'vert1',
      'vert2',
      'vertD',
      'compassX',
      'compassY',
      'compassZ',
      'horiz1',
      'horiz2',
      'horizD',
    ]
  ],
  ['MeasurementsUnits',
    [
      'time',
      'vert1',
      'vert2',
      'vertD',
      'compassX',
      'compassY',
      'compassZ',
      'horiz1',
      'horiz2',
      'horizD',
    ]
  ],
  ['ConductivityMeasurements',
    [
      'time',
      'vert1',
      'vert2',
    ]
  ],
  ['ConductivityMeasurementsUnits',
    [
      'time',
      'vert1',
      'vert2',
    ]
  ],
]

def csvFiles(request):
  csvFileNames = [
                 'Request',
                 'IridiumTransmission',
                 'RawPacket',
                 'PacketV6',
                 'PacketV6Units',
                 'Measurements',
                 'MeasurementsUnits',
                 'ConductivityMeasurements',
                 'ConductivityMeasurementsUnits',
                 ]
  context = {'csvFileNames': csvFileNames}
  return render(request, 'groundstation/csvFiles.html', context)

def naughtyFuncString(csvTableName, csvHeader):
  stringMan = ''
  stringMan = stringMan + 'def ' + csvTableName + '(request):\n'
  stringMan = stringMan + "filteredDataRows = {}\n"
  stringMan = stringMan + "  filteredDataRows['" + csvTableName + "'] = models." + csvTableName + ".objects.order_by('-time').all()\n"
  stringMan = stringMan + "  \n"
  stringMan = stringMan + "  csvHeader = [\n"
  for each in csvHeader:
   stringMan = stringMan + "              '" + each + "',\n"
  stringMan = stringMan + "              ]\n"
  stringMan = stringMan + "  csvData = [[\n"
  for each in csvHeader:
   stringMan = stringMan + "              x." + each + ",\n"
  stringMan = stringMan + "             ] for x in filteredDataRows['" + csvTableName + "']]\n"
  stringMan = stringMan + "  context = {'csvHeader':  csvHeader, 'csvData': csvData}\n"
  stringMan = stringMan + "  return render(request, 'groundstation/csvFile.csv', context)\n"
  stringMan = stringMan + "  \n"
  return stringMan
  
def Request(request):
  filteredDataRows = {}
  filteredDataRows['Request'] = models.Request.objects.order_by('-time').all()

  csvHeader = [
              'time',
              'processing_duration',
              'forwarded_for_address',
              'forwarded_host_address',
              'forwarded_server_address',
              'remote_address',
              'raw_request_data',
              'response_duration',
              'response_errors',
              'response_status_code',
              ]
  csvData = [[
              x.time,
              x.processing_duration,
              x.forwarded_for_address,
              x.forwarded_host_address,
              x.forwarded_server_address,
              x.remote_address,
              x.raw_request_data,
              x.response_duration,
              x.response_errors,
              x.response_status_code,
             ] for x in filteredDataRows['Request']]
  context = {'csvHeader':  csvHeader, 'csvData': csvData}
  return render(request, 'groundstation/csvFile.csv', context)

def IridiumTransmission(request):
  filteredDataRows = {}
  filteredDataRows['IridiumTransmission'] = models.IridiumTransmission.objects.order_by('-time').all()

  csvHeader = [
              'time',
              'latitude',
              'longitude',
              'cep',
              'momsn',
              'imei',
              'device_type',
              'serial',
              'iridium_session_status',
              'transmitted_via_satellite',
              ]
  csvData = [[
              x.time,
              x.latitude,
              x.longitude,
              x.cep,
              x.momsn,
              x.imei,
              x.device_type,
              x.serial,
              x.iridium_session_status,
              x.transmitted_via_satellite,
             ] for x in filteredDataRows['IridiumTransmission']]
  context = {'csvHeader':  csvHeader, 'csvData': csvData}
  return render(request, 'groundstation/csvFile.csv', context)

def RawPacket(request):
  filteredDataRows = {}
  filteredDataRows['RawPacket'] = models.RawPacket.objects.order_by('-time').all()

  csvHeader = [
              'hexdata',
              ]
  csvData = [[
              x.hexdata,
             ] for x in filteredDataRows['RawPacket']]
  context = {'csvHeader':  csvHeader, 'csvData': csvData}
  return render(request, 'groundstation/csvFile.csv', context)

def PacketV6(request):
  filteredDataRows = {}
  filteredDataRows['PacketV6'] = models.PacketV6.objects.order_by('-time').all()

  csvHeader = [
              'time',
              'yikes_status',
              'mcu_id',
              'version',
              'sequence_id',
              'latitude',
              'longitude',
              'altitude',
              'ballast_status',
              'cutdown_status',
              'conductivity_time',
              'satellites_count',
              'rockblock_signal_strength',
              'commands_count',
              'altimeter_temp',
              'altimeter_pressure',
              'positive_7v_battery_voltage',
              'negative_7v_battery_voltage',
              'positive_3v6_battery_voltage',
              'current_draw_7v_rail',
              'current_draw_3v3_rail',
              'battery_temp',
              'mcu_temp',
              'compass_temp',
              'adc1_temp',
              'adc2_temp',
              'external_temp',
              'rockblock_temp',
              ]
  csvData = [[
              x.time,
              x.yikes_status,
              x.mcu_id,
              x.version,
              x.sequence_id,
              x.latitude,
              x.longitude,
              x.altitude,
              x.ballast_status,
              x.cutdown_status,
              x.conductivity_time,
              x.satellites_count,
              x.rockblock_signal_strength,
              x.commands_count,
              x.altimeter_temp,
              x.altimeter_pressure,
              x.positive_7v_battery_voltage,
              x.negative_7v_battery_voltage,
              x.positive_3v6_battery_voltage,
              x.current_draw_7v_rail,
              x.current_draw_3v3_rail,
              x.battery_temp,
              x.mcu_temp,
              x.compass_temp,
              x.adc1_temp,
              x.adc2_temp,
              x.external_temp,
              x.rockblock_temp,
             ] for x in filteredDataRows['PacketV6']]
  context = {'csvHeader':  csvHeader, 'csvData': csvData}
  return render(request, 'groundstation/csvFile.csv', context)

def PacketV6Units(request):
  filteredDataRows = {}
  filteredDataRows['PacketV6Units'] = models.PacketV6Units.objects.order_by('-time').all()

  csvHeader = [
              'time',
              'yikes_status',
              'mcu_id',
              'version',
              'sequence_id',
              'latitude',
              'longitude',
              'altitude',
              'ballast_status',
              'cutdown_status',
              'conductivity_time',
              'satellites_count',
              'rockblock_signal_strength',
              'commands_count',
              'altimeter_temp',
              'altimeter_pressure',
              'positive_7v_battery_voltage',
              'negative_7v_battery_voltage',
              'positive_3v6_battery_voltage',
              'current_draw_7v_rail',
              'current_draw_3v3_rail',
              'battery_temp',
              'mcu_temp',
              'compass_temp',
              'adc1_temp',
              'adc2_temp',
              'external_temp',
              'rockblock_temp',
              ]
  csvData = [[
              x.time,
              x.yikes_status,
              x.mcu_id,
              x.version,
              x.sequence_id,
              x.latitude,
              x.longitude,
              x.altitude,
              x.ballast_status,
              x.cutdown_status,
              x.conductivity_time,
              x.satellites_count,
              x.rockblock_signal_strength,
              x.commands_count,
              x.altimeter_temp,
              x.altimeter_pressure,
              x.positive_7v_battery_voltage,
              x.negative_7v_battery_voltage,
              x.positive_3v6_battery_voltage,
              x.current_draw_7v_rail,
              x.current_draw_3v3_rail,
              x.battery_temp,
              x.mcu_temp,
              x.compass_temp,
              x.adc1_temp,
              x.adc2_temp,
              x.external_temp,
              x.rockblock_temp,
             ] for x in filteredDataRows['PacketV6Units']]
  context = {'csvHeader':  csvHeader, 'csvData': csvData}
  return render(request, 'groundstation/csvFile.csv', context)

def Measurements(request):
  filteredDataRows = {}
  filteredDataRows['Measurements'] = models.Measurements.objects.order_by('-time').all()

  csvHeader = [
              'time',
              'vert1',
              'vert2',
              'vertD',
              'compassX',
              'compassY',
              'compassZ',
              'horiz1',
              'horiz2',
              'horizD',
              ]
  csvData = [[
              x.time,
              x.vert1,
              x.vert2,
              x.vertD,
              x.compassX,
              x.compassY,
              x.compassZ,
              x.horiz1,
              x.horiz2,
              x.horizD,
             ] for x in filteredDataRows['Measurements']]
  context = {'csvHeader':  csvHeader, 'csvData': csvData}
  return render(request, 'groundstation/csvFile.csv', context)

def MeasurementsUnits(request):
  filteredDataRows = {}
  filteredDataRows['MeasurementsUnits'] = models.MeasurementsUnits.objects.order_by('-time').all()

  csvHeader = [
              'time',
              'vert1',
              'vert2',
              'vertD',
              'compassX',
              'compassY',
              'compassZ',
              'horiz1',
              'horiz2',
              'horizD',
              ]
  csvData = [[
              x.time,
              x.vert1,
              x.vert2,
              x.vertD,
              x.compassX,
              x.compassY,
              x.compassZ,
              x.horiz1,
              x.horiz2,
              x.horizD,
             ] for x in filteredDataRows['MeasurementsUnits']]
  context = {'csvHeader':  csvHeader, 'csvData': csvData}
  return render(request, 'groundstation/csvFile.csv', context)

def ConductivityMeasurements(request):
  filteredDataRows = {}
  filteredDataRows['ConductivityMeasurements'] = models.ConductivityMeasurements.objects.order_by('-time').all()

  csvHeader = [
              'time',
              'vert1',
              'vert2',
              ]
  csvData = [[
              x.time,
              x.vert1,
              x.vert2,
             ] for x in filteredDataRows['ConductivityMeasurements']]
  context = {'csvHeader':  csvHeader, 'csvData': csvData}
  return render(request, 'groundstation/csvFile.csv', context)

def ConductivityMeasurementsUnits(request):
  filteredDataRows = {}
  filteredDataRows['ConductivityMeasurementsUnits'] = models.ConductivityMeasurementsUnits.objects.order_by('-time').all()

  csvHeader = [
              'time',
              'vert1',
              'vert2',
              ]
  csvData = [[
              x.time,
              x.vert1,
              x.vert2,
             ] for x in filteredDataRows['ConductivityMeasurementsUnits']]
  context = {'csvHeader':  csvHeader, 'csvData': csvData}
  return render(request, 'groundstation/csvFile.csv', context)

def newGraph(request):

  #signal
  signal = request.GET.get('signal', '')
  #imei
  imei = request.GET.get('imei', '')
  #maxTime
  maxTime = request.GET.get('maxTime', '')
  #minTime
  minTime = request.GET.get('minTime', '')
  #maxVal
  maxVal = request.GET.get('maxVal', '')
  #minVal
  minVal = request.GET.get('minVal', '')
  #volts
  volts = request.GET.get('volts', '')
  
  if not signal:
    signal = 'horizontal'
  if not imei:
    imei = '*'
  if not minTime:
    minTime = (datetime.utcnow()-timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")
  if not maxTime:
    maxTime = '2020-07-11T00:00:00'
  if not maxVal:
    maxVal = None
  if not minVal:
    minVal = None
  #filtering volts
  if not volts:
    volts = 'False'
  elif volts == 'False':
    volts = 'False'
  elif volts == 'false':
    volts = 'False'
  elif volts == '0':
    volts = 'False'
  elif volts == 'f':
    volts = 'False'
  elif volts == 'F':
    volts = 'False'
  else:
    volts = 'True'
    
  #minTime filtering
  try:#second
    minTime = datetime.strptime(minTime,"%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)
  except:
    try:#minute
      minTime = datetime.strptime(minTime,"%Y-%m-%dT%H:%M").replace(tzinfo=dt.timezone.utc)
    except:
      try:#hour
        minTime = datetime.strptime(minTime,"%Y-%m-%dT%H").replace(tzinfo=dt.timezone.utc)
      except:
        try:#day
          minTime = datetime.strptime(minTime,"%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
        except:
          try:#month
            minTime = datetime.strptime(minTime,"%Y-%m").replace(tzinfo=dt.timezone.utc)
          except:#year
            minTime = datetime.strptime(minTime,"%Y").replace(tzinfo=dt.timezone.utc)
            
    #maxTime filtering
  try:#second
    maxTime = datetime.strptime(maxTime,"%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)
  except:
    try:#minute
      maxTime = datetime.strptime(maxTime,"%Y-%m-%dT%H:%M").replace(tzinfo=dt.timezone.utc)
    except:
      try:#hour
        maxTime = datetime.strptime(maxTime,"%Y-%m-%dT%H").replace(tzinfo=dt.timezone.utc)
      except:
        try:#day
          maxTime = datetime.strptime(maxTime,"%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
        except:
          try:#month
            maxTime = datetime.strptime(maxTime,"%Y-%m").replace(tzinfo=dt.timezone.utc)
          except:#year
            maxTime = datetime.strptime(maxTime,"%Y").replace(tzinfo=dt.timezone.utc)
              
  data = []
  onlyWantedData = []
  
  getParams = {
    'signal' :      signal ,
    'imei'   :      imei   ,
    'maxTime':      maxTime,
    'minTime':      minTime,
    'maxVal' :      maxVal ,
    'minVal' :      minVal ,
    'volts'  :      volts  ,
  }
  
  chart = None
  data_source = None
  
  chartTitle = "Title Here"
  chartDescription = "Description Here"
  chartOptions = {'title': chartTitle}
  

  if(signal in signalFunctions):
    chart, chartTitle, chartDescription, chartOptions = signalFunctions[signal](getParams)
  else:
    data = data + onlyWantedData
  
    data_source = SimpleDataSource(data=data)
    #data_source = ModelDataSource()
  
    chart = LineChart(data_source, options=chartOptions) # Creating a line chart
  
  chartOptions['title'] = chartTitle
  signalString = request.GET.get('signal','')
  
  horizontal =   True if signalString == 'horizontal' else False
  vertical =     True if signalString == 'vertical'   else False
  compass =    True if signalString == 'compass'    else False
  conductivity =   True if signalString == 'conductivity' else False
  gps =      True if signalString == 'gps'      else False
  gpsAltitude =      True if signalString == 'gpsAltitude'      else False
  iridium =    True if signalString == 'iridium'    else False
  cep =      True if signalString == 'cep'      else False
  termStatus = True if signalString == 'termStatus' else False
  supervision = True if signalString == 'supervision' else False
  supervisionPressure = True if signalString == 'supervisionPressure' else False
  supervisionTemp = True if signalString == 'supervisionTemp' else False
  
  
  context = {
    'chart': chart,
    'title': chartTitle,
    'description': chartDescription,
    'imei': imei,
    'maxTime': maxTime.strftime("%Y-%m-%dT%H:%M:%S"),
    'minTime': minTime.strftime("%Y-%m-%dT%H:%M:%S"),
    'maxVal': request.GET.get('maxVal',''),
    'minVal': request.GET.get('minVal',''),
    'volts': volts,
    'horizontal': horizontal,
    'vertical': vertical,
    'compass': compass,
    'conductivity': conductivity,
    'gps': gps,
    'gpsAltitude': gpsAltitude,
    'iridium': iridium,
    'cep': cep,
    'termStatus': termStatus,
    'supervision': supervision,
    'supervisionPressure': supervisionPressure,
    'supervisionTemp': supervisionTemp,
    }
  #if request.GET.get('maxTime',None):
  # context['maxTime'] = request.GET.get('maxTime',None)
  #if request.GET.get('minTime',None):
  # context['minTime'] = request.GET.get('minTime',None)

  return render(request, 'groundstation/newGraph.html', context)

def sillyJavascriptDatetimeString(datetimeObject):
  tDTS = datetimeObject.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
  tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
  return tempDateString

sJDS = sillyJavascriptDatetimeString
  
def descentRate(request):
  
  data = []
  dataUnits = models.PacketV6Units.objects.filter(parent_packet_v6__mcu_id=1).order_by('-time')[:400]
  dataUnits2 = []
  
  for each in dataUnits:
    dataUnits2.append([each.time,each.altitude])
    
  for each in range(len(dataUnits2)-10):
    differenceInAlts = (dataUnits2[each+10][1] - dataUnits2[each][1])/((dataUnits2[each+10][0] - dataUnits2[each][0]).total_seconds()/60.0)
    data.append([sJDS((dataUnits2[each][0]) + ((dataUnits2[each+10][0] - dataUnits2[each][0])/2)),differenceInAlts])
  
  print(len(dataUnits))
  print(len(data))
  dataHeader = [[{'type': 'datetime', 'label': 'Time'},'Alt']]
  dataList = dataHeader + data
  data_source = SimpleDataSource(data=dataList)
  chart = LineChart(data_source)

  context = {
  'chart': chart,
  'title': "Descent Rate",
  'description': "Descent Rate",
  }
  return render(request, 'groundstation/descentRate.html', context)
  
def avgBalloonLocation(request):
  
  data = []
  dataUnits = list(models.PacketV6Units.objects.filter(parent_packet_v6__mcu_id=1).order_by('-time')[:50])
  dataUnits.reverse()
  dataUnits2 = []
  
  totalPoints = 0.0
  totalLat = 0.0
  totalLon = 0.0
  totalAlt = 0.0
  
  for each in dataUnits:
    totalPoints = totalPoints + 1.0
    
    totalLat = totalLat + each.latitude
    totalLon = totalLon + each.longitude
    totalAlt = totalAlt + each.altitude
    
    
    
    dataUnits2.append([totalPoints,totalLat/totalPoints,totalLon/totalPoints,totalAlt/totalPoints])
    

    
  for each in dataUnits2:
    data.append([each[0],each[1],each[2],each[3]])
  
  print(len(dataUnits))
  print(len(data))
  dataHeader = [['Index','Longitude','Latitude','Altitude']]
  dataList = dataHeader + data
  data_source = SimpleDataSource(data=dataList)
  chart = LineChart(data_source)

  context = {
  'chart': chart,
  'title': "Avg. Position",
  'description': "Avg. Position",
  }
  return render(request, 'groundstation/descentRate.html', context)
  
def quickDescentRate(request):
  
  data = []
  dataUnits = models.PacketV6Units.objects.filter(parent_packet_v6__mcu_id=1).order_by('-time')[:50]
  dataUnits2 = []
  
  for each in dataUnits:
    dataUnits2.append([each.time,each.altitude])
    
  for each in range(len(dataUnits2)-1):
    differenceInAlts = (dataUnits2[each+1][1] - dataUnits2[each][1])/((dataUnits2[each+1][0] - dataUnits2[each][0]).total_seconds()/60.0)
    data.append([sJDS((dataUnits2[each][0]) + ((dataUnits2[each+1][0] - dataUnits2[each][0])/2)),differenceInAlts])
  
  print(len(dataUnits))
  print(len(data))
  dataHeader = [[{'type': 'datetime', 'label': 'Time'},'Alt']]
  dataList = dataHeader + data
  data_source = SimpleDataSource(data=dataList)
  chart = LineChart(data_source)

  context = {
  'chart': chart,
  'title': "Descent Rate",
  'description': "Descent Rate",
  }
  return render(request, 'groundstation/descentRate.html', context)
  
def timeSinceLastPacket(request):
  
  data = []
  dataUnits = models.PacketV6Units.objects.filter(parent_packet_v6__mcu_id=1).order_by('-time')[:400]
  dataUnits2 = []
  
  for each in dataUnits:
    dataUnits2.append([each.time,each.altitude])
    
  for each in range(len(dataUnits2)-1):
    differenceInAlts = (dataUnits2[each+1][1] - dataUnits2[each][1])/((dataUnits2[each+1][0] - dataUnits2[each][0]).total_seconds()/60.0)
    data.append([sJDS((dataUnits2[each][0]) + ((dataUnits2[each+1][0] - dataUnits2[each][0])/2)),differenceInAlts])
  
  print(len(dataUnits))
  print(len(data))
  dataHeader = [[{'type': 'datetime', 'label': 'Time'},'TimeSinceLastPacketV6','TimeSinceLastIridiumTransmission']]
  dataList = dataHeader + data
  data_source = SimpleDataSource(data=dataList)
  chart = LineChart(data_source)

  context = {
  'chart': chart,
  'title': "Descent Rate",
  'description': "Descent Rate",
  }
  return render(request, 'groundstation/descentRate.html', context)
  
  
def oldGoogleMap(request):
  
  
  
  points = [] #FORMAT OF '[Lat(float), Long(float), Name(String)],'
  
  ordered_gpsmeasurements = models.SlowMeasurement.objects.order_by('-global_id__global_id__transmit_time')[:400]
  
  for x in ordered_gpsmeasurements:
    tempDateTime = x.global_id.global_id.transmit_time
    #tDTS = tempDateTime.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
    #tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
    #tempDateString = "new Date(" + tempDateString[:4] + ".UTC" + tempDateString[4:] + ")"
    tempDateString = tempDateTime.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    realLong = x.gps_longitude
    longSign = 1.0
    realLat = x.gps_latitude
    latSign = 1.0
    
    if (x.gps_longitude > 0x80000000):
      realLong = x.gps_longitude - 0x80000000
      longSign = -1.0
    
    if (x.gps_latitude > 0x80000000):
      realLat = x.gps_latitude - 0x80000000
      latSign = -1.0
      
    realLongString = str(int(realLong)).zfill(9)
    realLatString = str(int(realLat)).zfill(9)
    
    print(realLongString)
    print(realLatString)
    
    realLong = longSign * (float(realLongString[0:3]) + (float(realLongString[3:5]) + float(realLongString[5:9])/10000.0 )/60.0)
    realLat = latSign * (float(realLatString[0:3]) + (float(realLatString[3:5]) + float(realLatString[5:9])/10000.0 )/60.0)
    
    altString = "Altitude: " + str(x.gps_altitude/10.0) + 'm'
    
    #descString = tempDateString + "<br>" + altString
    
    points.append([realLat, realLong, tempDateString, altString])#descString])#str(realLat) + ', ' + str(realLong) + ', '+ tempDateString])#tempDateString])
  
  context = {
    'points': points,
    'MAPS_API_KEY': secrets.MAPS_API_KEY,
  }
  return render(request, 'groundstation/googleMap.html', context)
  
def googleMap(request):
  
  formFields = {}
  
  formFields['mcuID'] = {}
  formFields['mcuID']['label'] = 'Packet MCU ID'
  formFields['mcuID']['options'] = ['ANY','1','2','3','4']
  formFields['mcuID']['selected'] = request.GET.get('mcuID', 'ANY')
  
  formFields['IMEI'] = {}
  formFields['IMEI']['label'] = 'Iridium IMEI'
  formFields['IMEI']['options'] = ['ANY', '300234065252710', '300434063219840', '300434063839690', '300434063766960', '300434063560100', '300434063184090', '300434063383330', '300434063185070', '300434063382350', '300234063778640', '888888888888888']
  formFields['IMEI']['selected'] = request.GET.get('IMEI', 'ANY')
  
  points = [] #FORMAT OF '[Lat(float), Long(float), Name(String)],'
  
  windowStartTimeString = '2019-08-29 00:00:00'
  windowStartTime = datetime.strptime(windowStartTimeString, "%Y-%m-%d %H:%M:%S")

  ordered_gpsmeasurements = models.PacketV6Units.objects.order_by('-time').filter(time__gte=windowStartTime)
  if(formFields['mcuID']['selected'] != 'ANY'):
    ordered_gpsmeasurements = ordered_gpsmeasurements.filter(parent_packet_v6__mcu_id=int(formFields['mcuID']['selected']))
  if(formFields['IMEI']['selected'] != 'ANY'):
    ordered_gpsmeasurements = ordered_gpsmeasurements.filter(parent_packet_v6__parent_transmission__imei=int(formFields['IMEI']['selected']))
  
  ordered_gpsmeasurements = ordered_gpsmeasurements[:400]
  
  for x in ordered_gpsmeasurements:
    tempDateTime = x.time
    tempDateString = tempDateTime.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    realLong = x.longitude
    realLat = x.latitude
    
    altString = "Altitude: " + str(x.altitude) + 'm'
    
    #descString = tempDateString + "<br>" + altString
    
    points.append([realLat, realLong, tempDateString, altString])#descString])#str(realLat) + ', ' + str(realLong) + ', '+ tempDateString])#tempDateString])
  
  context = {
    'points': points,
    'MAPS_API_KEY': secrets.MAPS_API_KEY,
    'FormFields': formFields,
  }
  return render(request, 'groundstation/googleMap.html', context)
  
def badGoogleMap(request):
  
  
  
  points = [] #FORMAT OF '[Lat(float), Long(float), Name(String)],'
  
  ordered_gpsmeasurements = models.SlowMeasurement.objects.order_by('-global_id__global_id__transmit_time')[:401]
  
  for x in ordered_gpsmeasurements:
    tempDateTime = x.global_id.global_id.transmit_time
    #tDTS = tempDateTime.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
    #tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
    #tempDateString = "new Date(" + tempDateString[:4] + ".UTC" + tempDateString[4:] + ")"
    tempDateString = tempDateTime.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    realLong = x.gps_longitude
    longSign = 1.0
    realLat = x.gps_latitude
    latSign = 1.0
    
    if (x.gps_longitude > 0x80000000):
      realLong = x.gps_longitude - 0x80000000
      longSign = -1.0
    
    if (x.gps_latitude > 0x80000000):
      realLat = x.gps_latitude - 0x80000000
      latSign = -1.0
      
    realLongString = str(int(realLong)).zfill(9)
    realLatString = str(int(realLat)).zfill(9)
    
    print(realLongString)
    print(realLatString)
    
    realLong = longSign * (float(realLongString[0:3]) + (float(realLongString[3:5]) + float(realLongString[5:9])/10000.0 )/60.0)
    realLat = latSign * (float(realLatString[0:3]) + (float(realLatString[3:5]) + float(realLatString[5:9])/10000.0 )/60.0)
    
    altString = "Altitude: " + str(x.gps_altitude/10.0) + 'm'
    
    #descString = tempDateString + "<br>" + altString
    
    points.append([x.global_id.global_id.iridium_latitude, x.global_id.global_id.iridium_longitude, tempDateString, altString])#descString])#str(realLat) + ', ' + str(realLong) + ', '+ tempDateString])#tempDateString])
  
  context = {
    'points': points,
    'MAPS_API_KEY': secrets.MAPS_API_KEY,
  }
  return render(request, 'groundstation/googleMap.html', context)
