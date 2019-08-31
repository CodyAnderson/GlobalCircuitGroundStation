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

signalDefinitions = {
                     'measurements_vert1': {
                                            'name': 'Vert1',
                                            'units': '',
                                            },
                     'measurements_vert2': {
                                            'name': 'Vert2',
                                            'units': '',
                                            }
                    }

def sillyJavascriptDatetimeString(datetimeObject):
  tDTS = datetimeObject.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
  tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
  return tempDateString

sJDS = sillyJavascriptDatetimeString

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
  
  dataHeader = [
			[{'type': 'datetime', 'label': 'Time'}, 'Volts +7V', toolTipColumn, 'Volts -7V', toolTipColumn, 'Volts +3V6', toolTipColumn]	 # create a list to hold the column names and data for the axis names
		]
  data = [[sJDS(x.time), x.positive_7v_battery_voltage, x.time.strftime("%b. %d, %Y, %H:%M:%S<br>" + "Volts +7V" + ": "+str(x.positive_7v_battery_voltage)), x.negative_7v_battery_voltage, x.time.strftime("%b. %d, %Y, %H:%M:%S<br>" + "Volts -7V" + ": "+str(x.negative_7v_battery_voltage)), x.positive_3v6_battery_voltage, x.time.strftime("%b. %d, %Y, %H:%M:%S<br>" + "Volts +3V6" + ": "+str(x.positive_3v6_battery_voltage))] for x in uncutData]

  # dataHeader = [
			# [{'type': 'datetime', 'label': 'Time'}, 'Volts +7V', 'Volts -7V', 'Volts +3V6']	 # create a list to hold the column names and data for the axis names
		# ]
  # data = [[sJDS(x.time), x.positive_7v_battery_voltage, x.negative_7v_battery_voltage, x.positive_3v6_battery_voltage] for x in uncutData]
  
  dataList = dataHeader + data
  
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
