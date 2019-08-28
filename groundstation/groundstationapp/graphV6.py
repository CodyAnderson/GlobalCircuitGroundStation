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

def graphV6(request):
  data = []
  onlyWantedData = []
  
  chart = None
  
  chartTitle = "Battery Voltage"
  chartDescription = "Measured voltages of the batteries."
  chartOptions = {'title': chartTitle}
  
  uncutData = models.PacketV6Units.objects.all()
  
  dataHeader = [
			[{'type': 'datetime', 'label': 'Time'}, 'Volts +7V', 'Volts -7V', 'Volts +3V6']	 # create a list to hold the column names and data for the axis names
		]
    
  data = [[x.time.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)"), x.positive_7v_battery_voltage, x.negative_7v_battery_voltage, x.positive_3v6_battery_voltage] for x in uncutData]
  
  dataList = dataHeader + data
  
  data_source = SimpleDataSource(data=dataList)
  
  chart = LineChart(data_source, options=chartOptions) # Creating a line chart
  
  chartOptions['title'] = chartTitle
  
  
  
  context = {
    'chart': chart,
    'title': chartTitle,
    'description': chartDescription,
    }
  #if request.GET.get('maxTime',None):
  # context['maxTime'] = request.GET.get('maxTime',None)
  #if request.GET.get('minTime',None):
  # context['minTime'] = request.GET.get('minTime',None)

  return render(request, 'groundstation/newGraph.html', context)
