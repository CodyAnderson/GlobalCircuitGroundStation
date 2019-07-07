from django.shortcuts import render

from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from graphos.renderers.gchart import LineChart

from . import models
from .imeiNames import imeiNames

import datetime as dt
from datetime import datetime
from datetime import timedelta

from .graphs.conductivity import conductivity
from .graphs.horizontal   import horizontal
from .graphs.vertical    import vertical
from .graphs.compass     import compass
from .graphs.cep       import cep
from .graphs.gps       import gps
from .graphs.termStatus import termStatus
from .graphs.supervision import supervision

signalFunctions = {
  'conductivity': conductivity,
  'horizontal'  : horizontal,
  'vertical'     : vertical,
  'compass'    : compass,
  'cep'      : cep,
  'gps'      : gps,
  'termStatus': termStatus,
  'supervision': supervision
  }



def newGraph(request):

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
  
  getParams = {
    'signal' :      signal ,
    'imei'   :      imei   ,
    'maxTime':      maxTime,
    'minTime':      minTime,
    'maxVal' :      maxVal ,
    'minVal' :      minVal ,
    'volts'  :      volts  ,
  }
  
  chart = None
  data_source = None
  
  chartTitle = "Title Here"
  chartDescription = "Description Here"
  chartOptions = {'title': chartTitle}
  

  if(signal in signalFunctions):
    chart, chartTitle, chartDescription, chartOptions = signalFunctions[signal](getParams)
  else:
    data = data + onlyWantedData
  
    data_source = SimpleDataSource(data=data)
    #data_source = ModelDataSource()
  
    chart = LineChart(data_source, options=chartOptions) # Creating a line chart
  
  chartOptions['title'] = chartTitle
  signalString = request.GET.get('signal','')
  
  horizontal =   True if signalString == 'horizontal' else False
  vertical =     True if signalString == 'vertical'   else False
  compass =    True if signalString == 'compass'    else False
  conductivity =   True if signalString == 'conductivity' else False
  gps =      True if signalString == 'gps'      else False
  iridium =    True if signalString == 'iridium'    else False
  cep =      True if signalString == 'cep'      else False
  termStatus = True if signalString == 'termStatus' else False
  supervision = True if signalString == 'supervision' else False
  
  
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
    'cep': cep,
    'termStatus': termStatus
    }
  #if request.GET.get('maxTime',None):
  # context['maxTime'] = request.GET.get('maxTime',None)
  #if request.GET.get('minTime',None):
  # context['minTime'] = request.GET.get('minTime',None)

  return render(request, 'groundstation/newGraph.html', context)
