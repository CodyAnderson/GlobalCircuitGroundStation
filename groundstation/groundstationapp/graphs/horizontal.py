from django.shortcuts import render

from django.db.models import DurationField, DateTimeField, ExpressionWrapper, F

from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from graphos.renderers.gchart import LineChart

from groundstationapp import models
from groundstationapp.imeiNames import imeiNames

import datetime as dt
from datetime import datetime
from datetime import timedelta

import time
	
def horizontal(getParams):
	
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
	chartTitle = "Horizontal Measurements"
	chartDescription = "This is a test graph generated from horizontal probe data.\n This is mostly for demonstration.\n Please enjoy."
	chartOptions = {'title': chartTitle}
	onlyWantedData = []
	dataHeader = [
			[{'type': 'datetime', 'label': 'Time'}, 'H1', 'H2', 'HD']	 # create a list to hold the column names and data for the axis names
		]
			
	
						
	#ordered_fastmeasurements = models.FastMeasurement.objects.filter(global_id__global_id__transmit_time__gte=minTime).filter(global_id__global_id__transmit_time__lte=maxTime).annotate(packet_transmit_time=F('global_id__global_id__transmit_time')).annotate(sample_delay=ExpressionWrapper(F('sub_id')*timedelta(seconds=5), output_field=DurationField())).annotate(sample_time=ExpressionWrapper(F('packet_transmit_time')+F('sample_delay'), output_field=DateTimeField())).order_by('global_id', 'sub_id')
	#print(ordered_fastmeasurements.query)
	#print('Annotated time: ' + str(ordered_fastmeasurements[0].sample_time))
	#x = ordered_fastmeasurements[0]
	#print('     Real time: ' + str(x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5)))
	#beforeTime = time.time()
	ordered_fastmeasurements = models.FastMeasurement.objects.filter(global_id__global_id__transmit_time__gte=minTime).filter(global_id__global_id__transmit_time__lte=maxTime).order_by('global_id__global_id__', 'sub_id').select_related('global_id').select_related('global_id__global_id')
	#x = ordered_fastmeasurements[0]
	#for x in ordered_fastmeasurements:
	#	realTime = x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5)
	#print('~~select_related~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	#print('     Real time: ' + str(x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5)))
	#print('  Elapsed time: ' + str(time.time()-beforeTime))
	
	#beforeTime = time.time()
	#ordered_fastmeasurements = models.FastMeasurement.objects.filter(global_id__global_id__transmit_time__gte=minTime).filter(global_id__global_id__transmit_time__lte=maxTime).order_by('global_id', 'sub_id')
	#for x in ordered_fastmeasurements:
	#	realTime = x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5)
	#x = ordered_fastmeasurements[0]
	#print('~~without select_related~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	#print('     Real time: ' + str(x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5)))
	#print('  Elapsed time: ' + str(time.time()-beforeTime))
	#print(ordered_fastmeasurements.query)
	#print()
	#print(ordered_fastmeasurements.query)
	scalar = 0.000125 if volts == 'True' else 1
	top = 99999 if not maxVal else float(maxVal)
	bottom = -99999 if not minVal else float(minVal)
	wantedimei = imei
	if(imei in imeiNames):
		wantedimei = imeiNames[imei]
	for x in ordered_fastmeasurements:
		if(wantedimei == '*' or wantedimei == str(x.global_id.global_id.imei)):
			tempDateTime = x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5)
			tDTS = tempDateTime.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
			tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
			onlyWantedData.append([tempDateString, x.horiz1*scalar, x.horiz2*scalar, x.horizD*scalar])

			
			
			
			
			
			
			
			
	data = dataHeader + onlyWantedData
	data_source = SimpleDataSource(data=data)
	chart = LineChart(data_source, options=chartOptions) # Creating a line chart

	return chart, chartTitle, chartDescription, chartOptions
