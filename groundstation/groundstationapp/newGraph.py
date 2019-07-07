from django.shortcuts import render

from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from graphos.renderers.gchart import LineChart

from . import models

import datetime as dt
from datetime import datetime
from datetime import timedelta

from .graphs.conductivity import conductivity, horizontal, vertical, compass, cep

signalFunctions = {
    'conductivity': conductivity,
    #'horizontal'  : horizontal,
    #'vertical'    : vertical,
    #'compass'     : compass,
    #'cep'         : cep
    }



def newGraph(request):

	imeiNames = {
		"CollinsLaptop": "8"*15,
		"GEC1": "0"*15,
		"GEC2": "9"*15,
		"TEMP_TEST_1": "0",
		"TestingRockBlock1": "300434063219840",
		"TestingRockBlock2": "300434063839690"
	}

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
		minTime = '2000-04-01T10:00:00'
	if not maxTime:
		maxTime = '2000-05-16T10:00:00'
	if not maxVal:
		maxVal = None
	if not minVal:
		minVal = None
	#filtering volts
	if not volts:
		volts = False
	elif volts == 'False':
		volts = False
	elif volts == 'false':
		volts = False
	elif volts == '0':
		volts = False
	elif volts == 'f':
		volts = False
	elif volts == 'F':
		volts = False
	else:
		volts = True
		
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
    
    getParams = {}
	
    chart = None
    data_source = None
    
	chartTitle = "Title Here"
	chartDescription = "Description Here"
	chartOptions = {'title': chartTitle}
    
    
    
    
    
    
    
    
    #chart, chartTitle, chartDescription, chartOptions = signalFunctions[signal](getParams)
    
    
    
    
    
	
	if(signal == 'vertical'):
		data = [
					[{'type': 'datetime', 'label': 'Time'}, 'V1', 'V2', 'VD']	 # create a list to hold the column names and data for the axis names
				]
				
		chartTitle = "Vertical Measurements"
		chartDescription = "This is a test graph generated from vertical probe data.\n This is mostly for demonstration.\n Please enjoy."
							
		ordered_fastmeasurements = models.FastMeasurement.objects.filter(global_id__global_id__transmit_time__gte=minTime).filter(global_id__global_id__transmit_time__lte=maxTime).order_by('global_id', 'sub_id')
		#print(ordered_fastmeasurements.query)
		scalar = 0.000125 if request.GET.get('volts','') == 'True' else 1
		top = 99999 if not request.GET.get('maxVal','') else float(request.GET.get('maxVal',''))
		bottom = -99999 if not request.GET.get('minVal','') else float(request.GET.get('minVal',''))
		wantedimei = imei
		if(imei in imeiNames):
			wantedimei = imeiNames[imei]
		for x in ordered_fastmeasurements:
			if(wantedimei == '*' or wantedimei == str(x.global_id.global_id.imei)):
				tempDateTime = x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5)
				tDTS = tempDateTime.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
				tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
				onlyWantedData.append([tempDateString, x.vert1*scalar, x.vert2*scalar, x.vertD*scalar])
	elif(signal == 'compass'):
		data = [
					[{'type': 'datetime', 'label': 'Time'}, 'CX', 'CY', 'CZ']	 # create a list to hold the column names and data for the axis names
				]
				
		chartTitle = "Magnetometer Compass Measurements"
		chartDescription = "This is a test graph generated from magnetometer compass readings.\n This is mostly for demonstration.\n Please enjoy."
							
		ordered_fastmeasurements = models.FastMeasurement.objects.filter(global_id__global_id__transmit_time__gte=minTime).filter(global_id__global_id__transmit_time__lte=maxTime).order_by('global_id', 'sub_id')
		#print(ordered_fastmeasurements.query)
		scalar = 0.000125 if request.GET.get('volts','') == 'True' else 1
		top = 99999 if not request.GET.get('maxVal','') else float(request.GET.get('maxVal',''))
		bottom = -99999 if not request.GET.get('minVal','') else float(request.GET.get('minVal',''))
		wantedimei = imei
		if(imei in imeiNames):
			wantedimei = imeiNames[imei]
		for x in ordered_fastmeasurements:
			if(wantedimei == '*' or wantedimei == str(x.global_id.global_id.imei)):
				tempDateTime = x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5)
				tDTS = tempDateTime.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
				tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
				onlyWantedData.append([tempDateString, x.compassX*scalar, x.compassY*scalar, x.compassZ*scalar])
	elif(signal == 'conductivity'):
		chart, chartTitle, chartDescription, chartOptions = signalFunctions[signal](getParams)
	#elif(signal == 'gps'):
	#elif(signal == 'iridium'):
	elif(signal == 'cep'):
		data = [
					[{'type': 'datetime', 'label': 'Time'}, 'CEP', 'Mins. since packet']	 # create a list to hold the column names and data for the axis names
				]
				
		chartTitle = "Iridium CEP"
		chartDescription = "This is a test graph generated from Iridium signal radius.\n This is mostly for demonstration.\n Please enjoy."
							
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
	else:
		signal = 'horizontal'
		data = [
					[{'type': 'datetime', 'label': 'Time'}, 'H1', 'H2', 'HD']	 # create a list to hold the column names and data for the axis names
				]
				
		chartTitle = "Horizontal Measurements"
		chartDescription = "This is a test graph generated from horizontal probe data.\n This is mostly for demonstration.\n Please enjoy."
							
		ordered_fastmeasurements = models.FastMeasurement.objects.filter(global_id__global_id__transmit_time__gte=minTime).filter(global_id__global_id__transmit_time__lte=maxTime).order_by('global_id', 'sub_id')
		#print(ordered_fastmeasurements.query)
		scalar = 0.000125 if request.GET.get('volts','') == 'True' else 1
		top = 99999 if not request.GET.get('maxVal','') else float(request.GET.get('maxVal',''))
		bottom = -99999 if not request.GET.get('minVal','') else float(request.GET.get('minVal',''))
		wantedimei = imei
		if(imei in imeiNames):
			wantedimei = imeiNames[imei]
		for x in ordered_fastmeasurements:
			if(wantedimei == '*' or wantedimei == str(x.global_id.global_id.imei)):
				tempDateTime = x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5)
				tDTS = tempDateTime.strftime("Date(%Y, %m, %d, %H, %M, %S, %f)")
				tempDateString = tDTS[:11] + '{0:02d}'.format(int(tDTS[11:13])-1) + tDTS[13:31] + '{0:03d}'.format(int(tDTS[31:37])//1000) + tDTS[37:]
				onlyWantedData.append([tempDateString, x.horiz1*scalar, x.horiz2*scalar, x.horizD*scalar])
	
	chartOptions['title'] = chartTitle
	#onlyWantedData.append([tempDateString,x.horiz1*scalar if x.horiz1*scalar <= top and x.horiz1*scalar >= bottom else top if x.horiz1*scalar > top else bottom,x.horiz2*scalar if x.horiz2*scalar <= top and x.horiz2*scalar >= bottom else top if x.horiz2*scalar > top else bottom,x.horizD*scalar if x.horizD*scalar <= top and x.horizD*scalar >= bottom else top if x.horizD*scalar > top else bottom])
	
	
	#onlyReallyWantedData = []
	#for x in onlyWantedData:
	#	if True: #if(x[0] >= minstringint and x[0] <= maxstringint):
	#		onlyReallyWantedData.append(x)
	#data = data + onlyReallyWantedData

	if(not signal == 'conductivity'):
		data = data + onlyWantedData
	
		data_source = SimpleDataSource(data=data)
		#data_source = ModelDataSource()
	
		chart = LineChart(data_source, options=chartOptions) # Creating a line chart
	
	
	signalString = request.GET.get('signal','')
	
	horizontal =	 True if signalString == 'horizontal'	else False
	vertical =		 True if signalString == 'vertical'		else False
	compass =		 True if signalString == 'compass'		else False
	conductivity =   True if signalString == 'conductivity' else False
	gps =			 True if signalString == 'gps'			else False
	iridium =		 True if signalString == 'iridium'		else False
	cep =			 True if signalString == 'cep'			else False
	
	
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
		'iridium': iridium,
		'cep': cep
		}
	#if request.GET.get('maxTime',None):
	#	context['maxTime'] = request.GET.get('maxTime',None)
	#if request.GET.get('minTime',None):
	#	context['minTime'] = request.GET.get('minTime',None)

	return render(request, 'groundstation/newGraph.html', context)
