# -*- coding: utf-8 -*-


from django.shortcuts import render

import MySQLdb
import time
import io

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart

from django.db.models import IntegerField, DateTimeField, ExpressionWrapper, F

from django.views.decorators.csrf import csrf_exempt

from . import structure
from . import models
import super_secrets as secrets

import datetime as dt
from datetime import datetime
from datetime import timedelta

import binascii

# Create your views here.

def homepage(request):
	#newIridiumData = models.IridiumData.objects.create(global_id=new_packet, transmit_time=datetime.utcnow(), iridium_latitude=0.1, iridium_longitude=1.0, iridium_cep=2.0, momsn=1, imei=999999999999999)
	#newSlowMeasurement = models.SlowMeasurement.objects.create(global_id=new_packet, gps_latitude=0.11, gps_longitude=1.01, gps_altitude=999.999, gps_time=datetime.utcnow()-timedelta(hours=1))
	
	#emptyString = "dead"
	#hexString = emptyString*(340//len(emptyString))
	
	#newRawData = models.RawData.objects.create(new_packet, data=?, hexData=hexString)
	
		
	
	
	print('Here it is, boys.')
	return render(request, 'groundstation/homepage.html')

def gps(request):		 # Change to google maps
	data = [
				['Time', 'Latitude', 'Longitude']	 # create a list to hold the column names and data for the axis names
			 ]
	
	db = MySQLdb.connect(host="localhost", user=secrets.sqluser,passwd=secrets.sqlpassword, db="groundstation") # Access the database to get all the current data
	cur = db.cursor()
	cur.execute('SELECT i.transmit_time,d.gps_latitude,d.gps_longitude,gps_altitude FROM groundstation.groundstationapp_slowmeasurement AS d INNER JOIN groundstationapp_iridiumdata AS i on i.global_id_id = d.global_id_id' )
	for row in cur.fetchall(): # going through each row
		l = []
		l.append(row[0]) # append each row to the data, only get the columns that we want
		l.append(row[1])
		l.append(row[2])
		data.append(l)
		
	db.close()
	data_source = SimpleDataSource(data=data)
	chart = LineChart(data_source, options={'title': "Coordinates"}) # Creating a line chart
	
	context = {'chart': chart}
	return render(request, 'groundstation/gps.html', context)	# rendering the chart when a request has gone through for this page, and using the mapPlot.html to render it

@csrf_exempt
def postfunc(request):
	if (request.POST):
		packet_data = request.POST.get('data')
		#if data exists
		if packet_data is not None:
			#packet_sio=io.StringIO(binascii.unhexlify(packet_data).decode(errors='ignore'))
			#packet_fields = structure.unpack(packet_sio)
			binary_packet_data = binascii.unhexlify(packet_data)
			packet_fields = structure.unpack_new(binary_packet_data)
			print(packet_fields['seq'])
			print(packet_fields['version'])
			timestring = request.POST.get('transmit_time')
			filteredImei = request.POST.get('imei')
			if(filteredImei == "CollinsLaptop"):
				filteredImei = "888888888888888"
			new_IridiumData = models.IridiumData.objects.create(transmit_time = timestring, iridium_latitude = request.POST.get('iridium_latitude'), iridium_longitude = request.POST.get('iridium_longitude'), iridium_cep = request.POST.get('iridium_cep'), momsn = request.POST.get('momsn'), imei = filteredImei, transmitted_via_satellite = True if request.POST.get('transmitted_via_satellite') is None else request.POST.get('transmitted_via_satellite'))
			print(new_IridiumData.transmit_time)
			new_Packet = models.Packet.objects.create(global_id=new_IridiumData,packet_id=packet_fields['seq'],version=packet_fields['version'])
			new_RawData = models.RawData.objects.create(global_id=new_Packet,data=binary_packet_data,hexdata=packet_data)
			hour_now = packet_fields['time']//10000
			minute_now = (packet_fields['time']-hour_now*10000)//100
			second_now = packet_fields['time']-hour_now*10000-minute_now*100
			time_now = datetime.utcnow().replace(hour=hour_now,minute=minute_now,second=second_now,microsecond=0)
			new_SlowMeasurement = models.SlowMeasurement.objects.create(global_id=new_Packet,gps_latitude=packet_fields['lat'],gps_longitude=packet_fields['lon'],gps_altitude=packet_fields['alt'],gps_time=time_now)
			for i in range(0,12):
				new_FastMeasurement = models.FastMeasurement.objects.create(global_id=new_Packet,sub_id=i,vert1=packet_fields['vert1'][i],vert2=packet_fields['vert2'][i],vertD=packet_fields['vertD'][i],compassX=packet_fields['compassX'][i],compassY=packet_fields['compassY'][i],compassZ=packet_fields['compassZ'][i],horiz1=packet_fields['horiz1'][i],horiz2=packet_fields['horiz2'][i],horizD=packet_fields['horizD'][i])
			for i in range(0,15):
				new_ConductivityData = models.ConductivityData.objects.create(global_id=new_Packet,sub_id=i*10+(packet_fields['seq']%10),vert1=packet_fields['cVert1'][i],vert2=packet_fields['cVert2'][i])
			labelList=["Temperature","Temperature","Pressure","Pressure","IL0","IL1","IL2","IH0","IH1","IH2","T0","T1","T2","Tmag","Tadc1","Tadc2","","","",""]
			newSupDataL= models.SupData.objects.create(global_id=new_Packet,sub_id=0,type=labelList[(packet_fields['seq']%10)*2], value=packet_fields['sup'][0])
			newSupDataH= models.SupData.objects.create(global_id=new_Packet,sub_id=0 if (packet_fields['seq']%10 > 1) else 1,type=labelList[((packet_fields['seq']%10)*2)+1], value=packet_fields['sup'][1])

		else:
			new_Packet = models.Packet.objects.create(packet_id=0xDEAD,version=0xDEAD)
		#else
		#iridium_txtime = request.POST.get('transmit_time',time.strftime("%Y-%m-%dT%H:%M:%SZ UTC",time.gmtime()))
		iridium_txtime = request.POST.get('transmit_time')
		iridium_imei = request.POST.get('imei')
		iridium_momsn = request.POST.get('momsn')
		iridium_latitude = request.POST.get('iridium_latitude')
		iridium_longitude = request.POST.get('iridium_longitude')
		iridium_cep = request.POST.get('iridium_cep')
		Data={'data':packet_data,'txtime':iridium_txtime,'imei':iridium_imei,'momsn':iridium_momsn,'lat':iridium_latitude,'lon':iridium_longitude,'cep':iridium_cep}
		#print(Data)
		
		print(packet_fields)
		context = {'text': Data}
	elif (request.GET):
		context = {'text': 'get'}
	else:
		context = {'text': 'none'}
	return render(request, 'groundstation/post.html', context)

def horizontal(request):
	data = [
				['Time', 'H1', 'H2', 'HD']	 # create a list to hold the column names and data for the axis names
			]
	minstringint = datetime.strptime(request.GET.get('min','2000-04-01T10:00:00'),"%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)
	maxstringint = datetime.strptime(request.GET.get('max','2020-05-16T10:00:00'),"%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)
	ordered_fastmeasurements = models.FastMeasurement.objects.filter(global_id__global_id__transmit_time__gte=minstringint).filter(global_id__global_id__transmit_time__lte=maxstringint).order_by('global_id', 'sub_id')
	#print(ordered_fastmeasurements.query)
	scalar = 0.000125 if request.GET.get('volts','') == 'True' else 1
	top = 99999 if not request.GET.get('top','') else float(request.GET.get('top',''))
	bottom = -99999 if not request.GET.get('bottom','') else float(request.GET.get('bottom',''))
	onlyWantedData = []
	wantedimei = request.GET.get('imei','*')
	if(wantedimei == "CollinsLaptop"):
		wantedimei = "888888888888888"
	for x in ordered_fastmeasurements:
		if(wantedimei == '*' or wantedimei == str(x.global_id.global_id.imei)):
			onlyWantedData.append([x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5),x.horiz1*scalar if x.horiz1*scalar <= top and x.horiz1*scalar >= bottom else top if x.horiz1*scalar > top else bottom,x.horiz2*scalar if x.horiz2*scalar <= top and x.horiz2*scalar >= bottom else top if x.horiz2*scalar > top else bottom,x.horizD*scalar if x.horizD*scalar <= top and x.horizD*scalar >= bottom else top if x.horizD*scalar > top else bottom])
	
	onlyReallyWantedData = []
	for x in onlyWantedData:
		if True: #if(x[0] >= minstringint and x[0] <= maxstringint):
			onlyReallyWantedData.append(x)
	data = data + onlyReallyWantedData
	
	chartTitle = "Horizontal Measurements"
	chartDescription = "This is a test graph generated from all of the fast measurement data.\n This is mostly for demonstration.\n Please enjoy."
	
	data_source = SimpleDataSource(data=data)
	chart = LineChart(data_source, options={'title': chartTitle}) # Creating a line chart
	
	context = {'chart': chart, 'title': chartTitle, 'description': chartDescription}

	return render(request, 'groundstation/graph.html', context)
	
def vertical(request):
	data = [
				['Time', 'V1', 'V2', 'VD']	 # create a list to hold the column names and data for the axis names
			]
	minstringint = datetime.strptime(request.GET.get('min','2000-01-01T10:00:00'),"%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)
	maxstringint = datetime.strptime(request.GET.get('max','2020-12-25T10:00:00'),"%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)
	ordered_fastmeasurements = models.FastMeasurement.objects.filter(global_id__global_id__transmit_time__gte=minstringint).filter(global_id__global_id__transmit_time__lte=maxstringint).order_by('global_id', 'sub_id')
	#print(len(ordered_fastmeasurements))
	scalar = 0.000125 if request.GET.get('volts','') == 'True' else 1
	top = 99999 if not request.GET.get('top','') else float(request.GET.get('top',''))
	bottom = -99999 if not request.GET.get('bottom','') else float(request.GET.get('bottom',''))
	onlyWantedData = []
	wantedimei = request.GET.get('imei','*')
	if(wantedimei == "CollinsLaptop"):
		wantedimei = "888888888888888"
	for x in ordered_fastmeasurements:
		if(wantedimei == '*' or wantedimei == str(x.global_id.global_id.imei)):
			onlyWantedData.append([x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5),x.vert1*scalar if x.vert1*scalar <= top and x.vert1*scalar >= bottom else top if x.vert1*scalar > top else bottom,x.vert2*scalar if x.vert2*scalar <= top and x.vert2*scalar >= bottom else top if x.vert2*scalar > top else bottom,x.vertD*scalar if x.vertD*scalar <= top and x.vertD*scalar >= bottom else top if x.vertD*scalar > top else bottom])
	#minstringint = int(request.GET.get('min','0'))
	#maxstringint = int(request.GET.get('max','999999'))
	wantedimei = request.GET.get('imei','*')
	onlyReallyWantedData = []
	for x in onlyWantedData:
		if True: #if(x[0] >= minstringint and x[0] <= maxstringint):
			onlyReallyWantedData.append(x)
	data = data + onlyReallyWantedData
	
	chartTitle = "Vertical Measurements"
	chartDescription = "This is a test graph generated from all of the fast measurement data.\n This is mostly for demonstration.\n Please enjoy."
	
	data_source = SimpleDataSource(data=data)
	chart = LineChart(data_source, options={'title': chartTitle}) # Creating a line chart
	
	context = {'chart': chart, 'title': chartTitle, 'description': chartDescription}
	return render(request, 'groundstation/graph.html', context)

def conductivity(request):
	data = [
				['Time', 'V1', 'V2' ]	 # create a list to hold the column names and data for the axis names
			]
	ordered_condmeasurements = models.ConductivityData.objects.order_by('global_id', 'sub_id')
	print(len(ordered_condmeasurements))
	onlyWantedData = [[x.global_id.id*12+x.sub_id,x.vert1,x.vert2] for x in ordered_condmeasurements]
	data = data + onlyWantedData
	
	chartTitle = "Conductivity Measurements"
	chartDescription = "This is a test graph generated from all of the conductivity measurement data.\n This is mostly for demonstration.\n Please enjoy."
	
	data_source = SimpleDataSource(data=data)
	chart = LineChart(data_source, options={'title': chartTitle}) # Creating a line chart
	
	context = {'chart': chart, 'title': chartTitle, 'description': chartDescription}
	return render(request, 'groundstation/graph.html',context)
    
    
    
def newGraph(request):
	data = [
				['Time', 'H1', 'H2', 'HD']	 # create a list to hold the column names and data for the axis names
			]
	minstringint = datetime.strptime(request.GET.get('minTime','2000-04-01T10:00:00'),"%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)
	maxstringint = datetime.strptime(request.GET.get('maxTime','2020-05-16T10:00:00'),"%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)
	ordered_fastmeasurements = models.FastMeasurement.objects.filter(global_id__global_id__transmit_time__gte=minstringint).filter(global_id__global_id__transmit_time__lte=maxstringint).order_by('global_id', 'sub_id')
	#print(ordered_fastmeasurements.query)
	scalar = 0.000125 if request.GET.get('volts','') == 'True' else 1
	top = 99999 if not request.GET.get('maxVal','') else float(request.GET.get('maxVal',''))
	bottom = -99999 if not request.GET.get('minVal','') else float(request.GET.get('minVal',''))
	onlyWantedData = []
	wantedimei = request.GET.get('imei','*')
	if(wantedimei == "CollinsLaptop"):
		wantedimei = "888888888888888"
	for x in ordered_fastmeasurements:
		if(wantedimei == '*' or wantedimei == str(x.global_id.global_id.imei)):
			onlyWantedData.append([x.global_id.global_id.transmit_time+x.sub_id*timedelta(seconds=5),x.horiz1*scalar if x.horiz1*scalar <= top and x.horiz1*scalar >= bottom else top if x.horiz1*scalar > top else bottom,x.horiz2*scalar if x.horiz2*scalar <= top and x.horiz2*scalar >= bottom else top if x.horiz2*scalar > top else bottom,x.horizD*scalar if x.horizD*scalar <= top and x.horizD*scalar >= bottom else top if x.horizD*scalar > top else bottom])
	
	onlyReallyWantedData = []
	for x in onlyWantedData:
		if True: #if(x[0] >= minstringint and x[0] <= maxstringint):
			onlyReallyWantedData.append(x)
	data = data + onlyReallyWantedData
	
	chartTitle = "Horizontal Measurements"
	chartDescription = "This is a test graph generated from all of the fast measurement data.\n This is mostly for demonstration.\n Please enjoy."
	
	data_source = SimpleDataSource(data=data)
	chart = LineChart(data_source, options={'title': chartTitle}) # Creating a line chart
	
	context = {'chart': chart, 'title': chartTitle, 'description': chartDescription, 'imei': request.GET.get('imei',''), 'maxTime': request.GET.get('maxTime',''), 'minTime': request.GET.get('minTime',''), 'maxVal': request.GET.get('maxVal',''), 'minVal': request.GET.get('minVal','')}

	return render(request, 'groundstation/newGraph.html', context)