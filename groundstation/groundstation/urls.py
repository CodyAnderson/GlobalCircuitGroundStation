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

from groundstationapp.views import homepage, gps, postfunc, horizontal, vertical, conductivity, newGraph, submitfunc, dumpfunc, scrapefunc

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
	url(r'^dump.json$', dumpfunc, name='dumpfunc'),
	url(r'^scrape/$', scrapefunc, name='scrapefunc'),
	url(r'^utf8.js$', utf8js, name='utf8js'),
]
