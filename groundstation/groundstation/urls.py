"""groundstation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from groundstationapp.views import homepage, gps, fastPost, horizontal, vertical, conductivity, submitfunc, dumpfunc, scrapefunc, utf8js, theBest, greyBalloon, redBalloon, greyBalloonClicked, redBalloonClicked, dashboard, dashboardV6, kmlFile
from groundstationapp.newGraph import newGraph, oldGoogleMap, googleMap, badGoogleMap, quickDescentRate, descentRate, avgBalloonLocation, csvFiles
from groundstationapp.newGraph import Request, IridiumTransmission, RawPacket, PacketV6, PacketV6Units, Measurements, MeasurementsUnits, ConductivityMeasurements, ConductivityMeasurementsUnits
from groundstationapp.newGraph import EverythingExceptForConductivity, FlightID_IMEI_Probe_Mag_RAW
from groundstationapp.graphV6 import graphV6

urlpatterns = [
  url(r'^$', homepage, name='homepage'),
  #url(r'^gps/$', gps, name='gps'),
  #url(r'^altitude/$', altitude, name='altitude'),
  url(r'^horizontal/$', horizontal, name='horizontal'),
  url(r'^vertical/$', vertical, name='vertical'),
  #url(r'^compass/$', compass, name='compass'),
  url(r'^conductivity/$', conductivity, name='conductivity'),
  url(r'^oldgraph/$', newGraph, name='oldGraph'),
  url(r'^newgraph/$', newGraph, name='newGraph'),
  url(r'^post/$', fastPost, name='fastPost'),
  url(r'^submit/$', submitfunc, name='submitfunc'),
  url(r'^submit/utf8\.js$', utf8js, name='utf8js'),
  url(r'^dump.hex$', dumpfunc, name='dumpfunc'),
  url(r'^dump.json$', dumpfunc, name='dumpfunc'),
  url(r'^theBest.json$', theBest, name='theBest'),
  url(r'^scrape/$', scrapefunc, name='scrapefunc'),
  url(r'^googleMap/$', googleMap, name='googleMap'),
  url(r'^oldGoogleMap/$', oldGoogleMap, name='oldGoogleMap'),
  url(r'^badGoogleMap/$', badGoogleMap, name='badGoogleMap'),
  url(r'^GreyBalloon.png$', greyBalloon, name='greyBalloon'),
  url(r'^RedBalloon.png$', redBalloon, name='redBalloon'),
  url(r'^GreyBalloonClicked.png$', greyBalloonClicked, name='greyBalloonClicked'),
  url(r'^RedBalloonClicked.png$', redBalloonClicked, name='redBalloonClicked'),
  url(r'^dashboard/$', dashboard, name='dashboard'),
  url(r'^dashboardV6/$', dashboardV6, name='dashboardV6'),
  url(r'^graphV6/$', graphV6, name='graphV6'),
  url(r'^descentRate/$', descentRate, name='descentRate'),
  url(r'^quickDescentRate/$', quickDescentRate, name='quickDescentRate'),
  url(r'^balloonPath\.kml', kmlFile, name='kmlFile'),
  url(r'^avgBalloonLocation/$', avgBalloonLocation, name='avgBalloonLocation'),
  url(r'^csvFiles/$', csvFiles, name='csvFiles'),
  url(r'^Request\.csv$', Request, name='Request'),
  url(r'^IridiumTransmission\.csv$', IridiumTransmission, name='IridiumTransmission'),
  url(r'^RawPacket\.csv$', RawPacket, name='RawPacket'),
  url(r'^PacketV6\.csv$', PacketV6, name='PacketV6'),
  url(r'^PacketV6Units\.csv$', PacketV6Units, name='PacketV6Units'),
  url(r'^Measurements\.csv$', Measurements, name='Measurements'),
  url(r'^MeasurementsUnits\.csv$', MeasurementsUnits, name='MeasurementsUnits'),
  url(r'^ConductivityMeasurements\.csv$', ConductivityMeasurements, name='ConductivityMeasurements'),
  url(r'^ConductivityMeasurementsUnits\.csv$', ConductivityMeasurementsUnits, name='ConductivityMeasurementsUnits'),
  
  url(r'^EverythingExceptForConductivity\.csv$', EverythingExceptForConductivity, name='EverythingExceptForConductivity'),
  url(r'^FlightID_IMEI_Probe_Mag_RAW\.csv$', FlightID_IMEI_Probe_Mag_RAW, name='FlightID_IMEI_Probe_Mag_RAW'),
  
  
]
