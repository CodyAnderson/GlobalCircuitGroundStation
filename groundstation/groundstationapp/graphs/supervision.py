from django.shortcuts import render

from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from graphos.renderers.gchart import LineChart

from groundstationapp import models
from groundstationapp.imeiNames import imeiNames

import datetime as dt
from datetime import datetime
from datetime import timedelta
  
def supervision(getParams):
  
  #signal
  signal = getParams['signal']
  #imei
  imei = getParams['imei']
  #maxTime
  maxTime = getParams['maxTime']
  #minTime
  minTime = getParams['minTime']
  #maxVal
  maxVal = getParams['maxVal']
  #minVal
  minVal = getParams['minVal']
  #volts
  volts = getParams['volts']
  
  chart = None
  chartTitle = "Supervision"
  chartDescription = "This is a test graph generated from supervision data.\n This is mostly for demonstration.\n Please enjoy."
  chartOptions = {'title': chartTitle}
  onlyWantedData = []
  dataHeader = [
      [{'type': 'datetime', 'label': 'Time'}, 'value', 'sequence', 'ID']   # create a list to hold the column names and data for the axis names
    ]
      
  
            
  supdata = models.SupData.objects.filter(global_id__global_id__transmit_time__gte=minTime).filter(global_id__global_id__transmit_time__lte=maxTime).order_by('global_id')
  #print(ordered_fastmeasurements.query)
  top = 99999 if not maxVal else float(maxVal)
  bottom = -99999 if not minVal else float(minVal)
  wantedimei = imei
  if(imei in imeiNames):
    wantedimei = imeiNames[imei]
  for x in supdata:
    if(wantedimei == '*' or wantedimei == str(x.global_id.global_id.imei)):
      if(((x.type=='Temperature' or x.type=='Pressure') and x.sub_id==0) or x.type=='IL0' or x.type=='IL2' or x.type=='IH1' or x.type=='T0' or x.type=='T2' or x.type=='Tadc1' or x.type=='Text' or x.type=='UNUSED0'):
        tempDateTime = x.global_id.global_id.transmit_time
        tDTS = tempDateTime.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
        tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
        onlyWantedData.append([tempDateString, x.value, x.global_id.packet_id%10, 0])
      else:
        tempDateTime = x.global_id.global_id.transmit_time + timedelta(seconds=30)
        tDTS = tempDateTime.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
        tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
        onlyWantedData.append([tempDateString, x.value, x.global_id.packet_id%10, 1])
  
  chartOptions["pointSize"]=5
  chartOptions["series"] = {0: {"targetAxisIndex": 0},1: {"targetAxisIndex": 1}, 2: {"targetAxisIndex": 1}}
  chartOptions["vAxes"] = {0: {"title": 'value'}, 1: {"title": 'sequence'}}    
  data = dataHeader + onlyWantedData
  data_source = SimpleDataSource(data=data)
  chart = LineChart(data_source, options=chartOptions) # Creating a line chart

  return chart, chartTitle, chartDescription, chartOptions
