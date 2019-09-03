import requests
import json

def kmlFileString():

  FileStart = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>Test.kml</name>
	<Style id="inline3">
		<LineStyle>
			<color>ffffffff</color>
			<width>2</width>
		</LineStyle>
		<PolyStyle>
			<fill>0</fill>
		</PolyStyle>
	</Style>
  <Style id="inline4">
		<LineStyle>
			<color>ffff0000</color>
			<width>2</width>
		</LineStyle>
		<PolyStyle>
			<fill>0</fill>
		</PolyStyle>
	</Style>
	<Style id="inline1">
		<LineStyle>
			<color>ff0000ff</color>
			<width>1</width>
		</LineStyle>
		<PolyStyle>
			<fill>0</fill>
		</PolyStyle>
	</Style>
	<Style id="inline10">
		<LineStyle>
			<color>ff00ffff</color>
			<width>1</width>
		</LineStyle>
		<PolyStyle>
			<fill>0</fill>
		</PolyStyle>
	</Style>
	<StyleMap id="inline">
		<Pair>
			<key>normal</key>
			<styleUrl>#inline1</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#inline00</styleUrl>
		</Pair>
	</StyleMap>
  <StyleMap id="inline2">
		<Pair>
			<key>normal</key>
			<styleUrl>#inline4</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#inline3</styleUrl>
		</Pair>
	</StyleMap>
	<StyleMap id="inline0">
		<Pair>
			<key>normal</key>
			<styleUrl>#inline10</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#inline01</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="inline00">
		<LineStyle>
			<color>ff0000ff</color>
			<width>1</width>
		</LineStyle>
		<PolyStyle>
			<fill>0</fill>
		</PolyStyle>
	</Style>
	<Style id="inline01">
		<LineStyle>
			<color>ff00ffff</color>
			<width>1</width>
		</LineStyle>
		<PolyStyle>
			<fill>0</fill>
		</PolyStyle>
	</Style>
"""

  FileEnd = """ </Document>
</kml>"""

  BalloonPathStart = """  <Placemark>
   <name>BalloonPathWithTime</name>
   <styleUrl>#inline2</styleUrl>
   <open>1</open>
   <gx:Track>
    <altitudeMode>absolute</altitudeMode>
"""
  BalloonPathEnd = """   </gx:Track>
  </Placemark>
"""

  CodyPath = """  <Placemark>
   <name>CodyPathWithTime</name>
   <styleUrl>#inline2</styleUrl>
   <open>1</open>
   <gx:Track>
    <altitudeMode>clampToGround</altitudeMode>
    <when>2019-09-02T17:50:00Z</when>
    <gx:coord>-121.54185199999999 44.301663399999995 947</gx:coord>
    <when>2019-09-03T17:44:41Z</when>
    <gx:coord>-121.5418492 44.3016104 944</gx:coord>
   </gx:Track>
  </Placemark>
"""
        
  TimeFormatString = """    <when>{YEAR}-{MONTH}-{DAY}T{HOUR}:{MIN}:{SEC}Z</when>
"""

  PointFormatString = """    <gx:coord>{LAT} {LONG} {ALT}</gx:coord>
"""
  SkyPathStart = """  
	<Placemark>
		<name>SkyPath</name>
		<styleUrl>#inline</styleUrl>
		<LineString>
			<extrude>1</extrude>
			<altitudeMode>absolute</altitudeMode>
			<coordinates>
				"""
        
        
  SkyPathEnd = """
			</coordinates>
		</LineString>
	</Placemark>
"""

  GroundPathStart = """  
	<Placemark>
		<name>GroundPath</name>
		<styleUrl>#inline0</styleUrl>
		<LineString>
			<extrude>1</extrude>
			<coordinates>
				"""
        
  GroundPathEnd = """
			</coordinates>
		</LineString>
	</Placemark>
"""

  PointString = "{1},{0},{2} "

# # Orig Begins at 2
# #   -> My edit begins at 247
# # Orig Ends at 373
# #   -> My edit ends at 323  
# points.reverse()
# points = points[245:-50]

  r = requests.get('https://gec.calamityconductor.com/googleMap/?mcuID=1&')
  x = r.text.split("['Lat', 'Long', 'Name', 'Marker'],\n               ")[1].split(',\n            ]);')[0]
  y = "{'array' : [" + x + "]}"
  z = y.replace("'",'"')
  a = json.loads(z)
  
  points = a['array']
  points.reverse()
  
  outfile = ""

  outfile = (outfile + FileStart)
  #outfile = (outfile + CodyPath)
  outfile = (outfile + BalloonPathStart)
  for each in range(len(points)):
    thisDict = {}
    
    dateTimeString = points[each][2].split(' UTC')[0]
    dateString, timeString = dateTimeString.split(' ')
    
    
    thisDict['YEAR'], thisDict['MONTH'], thisDict['DAY'] = dateString.split('-')
    thisDict['HOUR'], thisDict['MIN'], thisDict['SEC'] = timeString.split(':')

    thisDict['LAT'] = points[each][1]
    thisDict['LONG'] = points[each][0]
    thisDict['ALT'] = points[each][2].split(': ')[1].split('m')[0]
    outfile = (outfile + TimeFormatString.format(**thisDict))
    outfile = (outfile + PointFormatString.format(**thisDict))
  
  outfile = (outfile + BalloonPathEnd)
  
  outfile = (outfile + SkyPathStart)
  for each in range(len(points)):
    outfile = (outfile + PointString.format(points[each][0], points[each][1], points[each][2].split(': ')[1].split('m')[0]))
  outfile = (outfile + SkyPathEnd)
  
  outfile = (outfile + GroundPathStart)
  for each in range(len(points)):
    outfile = (outfile + PointString.format(points[each][0], points[each][1], points[each][2].split(': ')[1].split('m')[0]))
  outfile = (outfile + GroundPathEnd)
  
  
  outfile = (outfile + FileEnd)
  return outfile
  