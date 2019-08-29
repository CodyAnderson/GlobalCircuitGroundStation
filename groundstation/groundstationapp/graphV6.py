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

def sillyJavascriptDatetimeString(datetimeObject):
  tDTS = datetimeObject.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
  tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
  return tempDateString

sJDS = sillyJavascriptDatetimeString

def graphV6(request):
  data = []
  onlyWantedData = []
  
  chart = None
  
  chartTitle = "Battery Voltage"
  chartDescription = "Measured voltages of the batteries."
  chartOptions = {'title': chartTitle}
  
  
  
  uncutData = models.PacketV6Units.objects.filter(time__gte=datetime(2019, 8, 29)).all()
  
  dataHeader = [
			[{'type': 'datetime', 'label': 'Time'}, 'Volts +7V', {'type': 'string', 'role':'tooltip'}, 'Volts -7V', {'type': 'string', 'role':'tooltip'}, 'Volts +3V6', {'type': 'string', 'role':'tooltip'}]	 # create a list to hold the column names and data for the axis names
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
  
  chart = LineChart(data_source, options=chartOptions) # Creating a line chart
  
  
  
  
  
  context = {
    'chart': chart,
    'title': chartTitle,
    'description': chartDescription,
    }
  #if request.GET.get('maxTime',None):
  # context['maxTime'] = request.GET.get('maxTime',None)
  #if request.GET.get('minTime',None):
  # context['minTime'] = request.GET.get('minTime',None)

  return render(request, 'groundstation/graphV6.html', context)
