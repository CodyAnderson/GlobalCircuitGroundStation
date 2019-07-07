from django.shortcuts import render

from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from graphos.renderers.gchart import LineChart

from groundstationapp import models
from groundstationapp.imeiNames import imeiNames

import datetime as dt
from datetime import datetime
from datetime import timedelta
	
def cep(getParams):
	
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
	chartTitle = "Iridium CEP"
	chartDescription = "This is a test graph generated from Iridium signal radius.\n This is mostly for demonstration.\n Please enjoy."
	chartOptions = {'title': chartTitle}
	onlyWantedData = []
	dataHeader = [
		[{'type': 'datetime', 'label': 'Time'}, 'CEP', 'Mins. since packet']	 # create a list to hold the column names and data for the axis names
	]
			
	
						
	ordered_fastmeasurements = models.IridiumData.objects.filter(transmit_time__gte=minTime).filter(transmit_time__lte=maxTime).order_by('transmit_time')
	#print(ordered_fastmeasurements.query)
	wantedimei = imei
	if(imei in imeiNames):
		wantedimei = imeiNames[imei]
	prevTime = ordered_fastmeasurements[0].transmit_time
	for x in ordered_fastmeasurements:
		if(wantedimei == '*' or wantedimei == str(x.imei)):
			tempDateTime = x.transmit_time
			tDTS = tempDateTime.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
			tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
			deltaSinceLastPacket = tempDateTime-prevTime
			prevTime = tempDateTime
			minutesSinceLastPacket = float(deltaSinceLastPacket.total_seconds())/60.0
			
			
			
			
			
			
			
			onlyWantedData.append([tempDateString, x.iridium_cep, minutesSinceLastPacket])
			
	chartOptions["series"] = {0: {"targetAxisIndex": 0},1: {"targetAxisIndex": 1}}
	chartOptions["vAxes"] = {0: {"title": 'Iridium CEP (inverse signal strength (km))'}, 1: {"title": 'Time since packet (minutes)'}}
	onlyWantedData[0][2] = 0.0


			
			
			
			
			
			
			
			
	data = dataHeader + onlyWantedData
	data_source = SimpleDataSource(data=data)
	chart = LineChart(data_source, options=chartOptions) # Creating a line chart

	return chart, chartTitle, chartDescription, chartOptions
							
		
	