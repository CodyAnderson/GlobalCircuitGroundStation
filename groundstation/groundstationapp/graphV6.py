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

signalList = [
              'NONE'                                        ,
              'Request___processing_duration'               ,
              'Request___forwarded_for_address'             ,
              'Request___remote_address'                    ,
              'Request___response_duration'                 ,
              'Request___response_status_code'              ,
              
              
              
              'IridiumTransmission___latitude'              ,
              'IridiumTransmission___longitude'             ,
              'IridiumTransmission___cep'                   ,
              'IridiumTransmission___momsn'                 ,
              'IridiumTransmission___imei'                  ,
              'IridiumTransmission___device_type'           ,
              'IridiumTransmission___serial'                ,
              'IridiumTransmission___iridium_session_status',
              
              
              
              'PacketV6___yikes_status'                     ,
              'PacketV6___mcu_id'                           ,
              'PacketV6___version'                          ,
              'PacketV6___sequence_id'                      ,
              'PacketV6___latitude'                         ,
              'PacketV6___longitude'                        ,
              'PacketV6___altitude'                         ,
              'PacketV6___ballast_status'                   ,
              'PacketV6___cutdown_status'                   ,
              'PacketV6___conductivity_time'                ,
              'PacketV6___satellites_count'                 ,
              'PacketV6___rockblock_signal_strength'        ,
              'PacketV6___commands_count'                   ,
              'PacketV6___altimeter_temp'                   ,
              'PacketV6___altimeter_pressure'               ,
              'PacketV6___positive_7v_battery_voltage'      ,
              'PacketV6___negative_7v_battery_voltage'      ,
              'PacketV6___positive_3v6_battery_voltage'     ,
              'PacketV6___current_draw_7v_rail'             ,
              'PacketV6___current_draw_3v3_rail'            ,
              'PacketV6___battery_temp'                     ,
              'PacketV6___mcu_temp'                         ,
              'PacketV6___compass_temp'                     ,
              'PacketV6___adc1_temp'                        ,
              'PacketV6___adc2_temp'                        ,
              'PacketV6___external_temp'                    ,
              'PacketV6___rockblock_temp'                   ,
              
              'PacketV6Units___latitude'                    ,
              'PacketV6Units___longitude'                   ,
              'PacketV6Units___altitude'                    ,
              'PacketV6Units___conductivity_time'           ,
              'PacketV6Units___satellites_count'            ,
              'PacketV6Units___rockblock_signal_strength'   ,
              'PacketV6Units___commands_count'              ,
              'PacketV6Units___altimeter_temp'              ,
              'PacketV6Units___altimeter_pressure'          ,
              'PacketV6Units___positive_7v_battery_voltage' ,
              'PacketV6Units___negative_7v_battery_voltage' ,
              'PacketV6Units___positive_3v6_battery_voltage',
              'PacketV6Units___current_draw_7v_rail'        ,
              'PacketV6Units___current_draw_3v3_rail'       ,
              'PacketV6Units___battery_temp'                ,
              'PacketV6Units___mcu_temp'                    ,
              'PacketV6Units___compass_temp'                ,
              'PacketV6Units___adc1_temp'                   ,
              'PacketV6Units___adc2_temp'                   ,
              'PacketV6Units___external_temp'               ,
              'PacketV6Units___rockblock_temp'              ,
              
              
              
              'Measurements___vert1'                        ,
              'Measurements___vert2'                        ,
              'Measurements___vertD'                        ,
              'Measurements___compassX'                     ,
              'Measurements___compassY'                     ,
              'Measurements___compassZ'                     ,
              'Measurements___horiz1'                       ,
              'Measurements___horiz2'                       ,
              'Measurements___horizD'                       ,
              
              'MeasurementsUnits___vert1'                   ,
              'MeasurementsUnits___vert2'                   ,
              'MeasurementsUnits___vertD'                   ,
              'MeasurementsUnits___compassX'                ,
              'MeasurementsUnits___compassY'                ,
              'MeasurementsUnits___compassZ'                ,
              'MeasurementsUnits___horiz1'                  ,
              'MeasurementsUnits___horiz2'                  ,
              'MeasurementsUnits___horizD'                  ,
              
              
              
              'ConductivityMeasurements___vert1'            ,
              'ConductivityMeasurements___vert2'            ,
              
              'ConductivityMeasurementsUnits___vert1'       ,
              'ConductivityMeasurementsUnits___vert2'       ,
              ]

signalDefinitions = {
                    'NONE'                                        : None,
                    'Request___processing_duration'               :{
                                                                   'name' : 'Request Processing Duration',
                                                                   'units' : 's',
                                                                   },
                    'Request___forwarded_for_address'             :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Request___remote_address'                    :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Request___response_duration'                 :{
                                                                   'name' : '',
                                                                   'units' : 's',
                                                                   },
                    'Request___response_status_code'              :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'IridiumTransmission___latitude'              :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'IridiumTransmission___longitude'             :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'IridiumTransmission___cep'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'IridiumTransmission___momsn'                 :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'IridiumTransmission___imei'                  :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'IridiumTransmission___device_type'           :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'IridiumTransmission___serial'                :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'IridiumTransmission___iridium_session_status':{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___yikes_status'                     :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___mcu_id'                           :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___version'                          :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___sequence_id'                      :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___latitude'                         :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___longitude'                        :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___altitude'                         :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___ballast_status'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___cutdown_status'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___conductivity_time'                :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___satellites_count'                 :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___rockblock_signal_strength'        :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___commands_count'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___altimeter_temp'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___altimeter_pressure'               :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___positive_7v_battery_voltage'      :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___negative_7v_battery_voltage'      :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___positive_3v6_battery_voltage'     :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___current_draw_7v_rail'             :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___current_draw_3v3_rail'            :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___battery_temp'                     :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___mcu_temp'                         :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___compass_temp'                     :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___adc1_temp'                        :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___adc2_temp'                        :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___external_temp'                    :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6___rockblock_temp'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___latitude'                    :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___longitude'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___altitude'                    :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___conductivity_time'           :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___satellites_count'            :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___rockblock_signal_strength'   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___commands_count'              :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___altimeter_temp'              :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___altimeter_pressure'          :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___positive_7v_battery_voltage' :{
                                                                   'name' : 'Volts +7V',
                                                                   'units' : 'V',
                                                                   },
                    'PacketV6Units___negative_7v_battery_voltage' :{
                                                                   'name' : 'Volts -7V',
                                                                   'units' : 'V',
                                                                   },
                    'PacketV6Units___positive_3v6_battery_voltage':{
                                                                   'name' : 'Volts +3V6',
                                                                   'units' : 'V',
                                                                   },
                    'PacketV6Units___current_draw_7v_rail'        :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___current_draw_3v3_rail'       :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___battery_temp'                :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___mcu_temp'                    :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___compass_temp'                :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___adc1_temp'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___adc2_temp'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___external_temp'               :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'PacketV6Units___rockblock_temp'              :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Measurements___vert1'                        :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Measurements___vert2'                        :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Measurements___vertD'                        :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Measurements___compassX'                     :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Measurements___compassY'                     :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Measurements___compassZ'                     :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Measurements___horiz1'                       :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Measurements___horiz2'                       :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'Measurements___horizD'                       :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'MeasurementsUnits___vert1'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'MeasurementsUnits___vert2'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'MeasurementsUnits___vertD'                   :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'MeasurementsUnits___compassX'                :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'MeasurementsUnits___compassY'                :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'MeasurementsUnits___compassZ'                :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'MeasurementsUnits___horiz1'                  :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'MeasurementsUnits___horiz2'                  :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'MeasurementsUnits___horizD'                  :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'ConductivityMeasurements___vert1'            :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'ConductivityMeasurements___vert2'            :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'ConductivityMeasurementsUnits___vert1'       :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    'ConductivityMeasurementsUnits___vert2'       :{
                                                                   'name' : '',
                                                                   'units' : '',
                                                                   },
                    }
                    
def sillyJavascriptDatetimeString(datetimeObject):
  tDTS = datetimeObject.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
  tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
  return tempDateString

sJDS = sillyJavascriptDatetimeString

def signalValue(dataRow, signalId):
  if signalId == 'PacketV6Units___positive_7v_battery_voltage':
    return dataRow.positive_7v_battery_voltage
  elif signalId == 'PacketV6Units___negative_7v_battery_voltage':
    return dataRow.negative_7v_battery_voltage
  elif signalId == 'PacketV6Units___positive_3v6_battery_voltage':
    return dataRow.positive_3v6_battery_voltage
  
  return None
  
  
def graphV6(request):
  data = []
  onlyWantedData = []
  
  chart = None
  
  
  formFields = {}
  
  formFields['mcuID'] = {}
  formFields['mcuID']['label'] = 'Packet MCU ID'
  formFields['mcuID']['options'] = ['ANY','1','2','3','4']
  formFields['mcuID']['selected'] = request.GET.get('mcuID', 'ANY')
  
  formFields['IMEI'] = {}
  formFields['IMEI']['label'] = 'Iridium IMEI'
  formFields['IMEI']['options'] = ['ANY', '300234065252710', '300434063219840', '300434063839690', '300434063766960', '300434063560100', '300434063184090', '300434063383330', '300434063185070', '300434063382350', '300234063778640', '888888888888888']
  formFields['IMEI']['selected'] = request.GET.get('IMEI', 'ANY')
  
  formFields['leftAxisSignal_A'] = {}
  formFields['leftAxisSignal_A']['label'] = 'Left Axis Signal A'
  formFields['leftAxisSignal_A']['options'] = signalList
  formFields['leftAxisSignal_A']['selected'] = request.GET.get('leftAxisSignal_A', 'ANY')
  
  formFields['leftAxisSignal_B'] = {}
  formFields['leftAxisSignal_B']['label'] = 'Left Axis Signal B'
  formFields['leftAxisSignal_B']['options'] = signalList
  formFields['leftAxisSignal_B']['selected'] = request.GET.get('leftAxisSignal_B', 'ANY')
  
  formFields['leftAxisSignal_C'] = {}
  formFields['leftAxisSignal_C']['label'] = 'Left Axis Signal C'
  formFields['leftAxisSignal_C']['options'] = signalList
  formFields['leftAxisSignal_C']['selected'] = request.GET.get('leftAxisSignal_C', 'ANY')
  
  chartTitle = "Battery Voltage"
  chartDescription = "Measured voltages of the batteries."
  chartOptions = {'title': chartTitle}
  
  
  
  uncutData = models.PacketV6Units.objects.filter(time__gte=datetime(2019, 8, 29)).all()
  
  toolTipColumn = {'type': 'string', 'role':'tooltip', 'p':{'html': True}}
  
  
  dataHeader = [[{'type': 'datetime', 'label': 'Time'}]]
  
  #Loop through all the selected signals to create the dataHeader
  for signal in ['leftAxisSignal_A', 'leftAxisSignal_B', 'leftAxisSignal_C']:
    signalId = formFields[signal]['selected']
    if( signalId == 'ANY'):
      continue
    sigDef = signalDefinitions[signalId]
    dataHeader[0].append(sigDef['name'])
    dataHeader[0].append(toolTipColumn)
  dataHeader[0].append('TestBoi')
  dataArray = []
    
  #Loop through all the data
  for x in uncutData:
    data = [sJDS(x.time)]
    #Loop through all the selected signals to create the data array
    for signal in ['leftAxisSignal_A', 'leftAxisSignal_B', 'leftAxisSignal_C']:
      signalId = formFields[signal]['selected']
      if( signalId == 'ANY'):
        continue
      sigDef = signalDefinitions[signalId]
      sigName = sigDef['name']
      sigUnits = sigDef['units']
      sigValue = signalValue(x,signalId)
      data.append(sigValue)
      toolTipString = x.time.strftime("%b. %d, %Y, %H:%M:%S<br>" + sigName + ": "+str(sigValue))
      if(sigUnits):
        toolTipString = toolTipString + ' ' + sigUnits
      data.append(toolTipString)
    data.append(None)
    dataArray.append(data)
  for each in range(10):
    dataArray[each][7] = each
  dataList = dataHeader + dataArray
      
  # dataHeader = [
			# [{'type': 'datetime', 'label': 'Time'}, 'Volts +7V', toolTipColumn, 'Volts -7V', toolTipColumn, 'Volts +3V6', toolTipColumn]	 # create a list to hold the column names and data for the axis names
		# ]
  # data = [[sJDS(x.time), x.positive_7v_battery_voltage, x.time.strftime("%b. %d, %Y, %H:%M:%S<br>" + "Volts +7V" + ": "+str(x.positive_7v_battery_voltage)), x.negative_7v_battery_voltage, x.time.strftime("%b. %d, %Y, %H:%M:%S<br>" + "Volts -7V" + ": "+str(x.negative_7v_battery_voltage)), x.positive_3v6_battery_voltage, x.time.strftime("%b. %d, %Y, %H:%M:%S<br>" + "Volts +3V6" + ": "+str(x.positive_3v6_battery_voltage))] for x in uncutData]

  # # dataHeader = [
			# # [{'type': 'datetime', 'label': 'Time'}, 'Volts +7V', 'Volts -7V', 'Volts +3V6']	 # create a list to hold the column names and data for the axis names
		# # ]
  # # data = [[sJDS(x.time), x.positive_7v_battery_voltage, x.negative_7v_battery_voltage, x.positive_3v6_battery_voltage] for x in uncutData]
  
  # dataList = dataHeader + data
  
  data_source = SimpleDataSource(data=dataList)
  
  chartOptions['title'] = chartTitle
  chartOptions['tooltip'] = {'isHtml': True}
  chartOptions['hAxis'] = {'format': 'MMM. dd, yyyy, HH:mm:ss'}
  chartOptions["pointSize"] = 3
  
  chart = LineChart(data_source, options=chartOptions) # Creating a line chart
  
  
  
  
  context = {
    'chart': chart,
    'title': chartTitle,
    'description': chartDescription,
    'hours': [str(x).zfill(2) for x in range(24)],
    'minutes': [str(x).zfill(2) for x in range(60)],
    'seconds': [str(x).zfill(2) for x in range(60)],
    'FormFields': formFields
    }
  #if request.GET.get('maxTime',None):
  # context['maxTime'] = request.GET.get('maxTime',None)
  #if request.GET.get('minTime',None):
  # context['minTime'] = request.GET.get('minTime',None)

  return render(request, 'groundstation/graphV6.html', context)
