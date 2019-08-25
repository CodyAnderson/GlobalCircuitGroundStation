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

from groundstationapp.views import homepage, gps, postfunc, horizontal, vertical, conductivity, submitfunc, dumpfunc, scrapefunc, utf8js, theBest, greyBalloon, redBalloon, greyBalloonClicked, redBalloonClicked, dashboard, dashboardV6
from groundstationapp.newGraph import newGraph, googleMap, badGoogleMap

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    #url(r'^gps/$', gps, name='gps'),
	#url(r'^altitude/$', altitude, name='altitude'),
	url(r'^horizontal/$', horizontal, name='horizontal'),
	url(r'^vertical/$', vertical, name='vertical'),
	#url(r'^compass/$', compass, name='compass'),
	url(r'^conductivity/$', conductivity, name='conductivity'),
	url(r'^newgraph/$', newGraph, name='newGraph'),
    url(r'^post/$', postfunc, name='postfunc'),
	url(r'^submit/$', submitfunc, name='submitfunc'),
	url(r'^submit/utf8\.js$', utf8js, name='utf8js'),
	url(r'^dump.hex$', dumpfunc, name='dumpfunc'),
	url(r'^dump.json$', dumpfunc, name='dumpfunc'),
	url(r'^theBest.json$', theBest, name='theBest'),
	url(r'^scrape/$', scrapefunc, name='scrapefunc'),
	url(r'^googleMap/$', googleMap, name='googleMap'),
	url(r'^badGoogleMap/$', badGoogleMap, name='badGoogleMap'),
	url(r'^GreyBalloon.png$', greyBalloon, name='greyBalloon'),
	url(r'^RedBalloon.png$', redBalloon, name='redBalloon'),
	url(r'^GreyBalloonClicked.png$', greyBalloonClicked, name='greyBalloonClicked'),
	url(r'^RedBalloonClicked.png$', redBalloonClicked, name='redBalloonClicked'),
	url(r'^dashboard/$', dashboard, name='dashboard'),
	url(r'^dashboardV6/$', dashboardV6, name='dashboardV6'),
]
