import struct

PACKET_VERSION=3
def unpack(f):
    values={}
    values['version']=struct.unpack('<B',f.read(1))[0]
    values['yikes']=struct.unpack('<B',f.read(1))[0]
    values['seq']=struct.unpack('<H',f.read(2))[0]
    values['time']=struct.unpack('<I',f.read(4))[0]
    values['lat']=struct.unpack('<I',f.read(4))[0]
    values['lon']=struct.unpack('<I',f.read(4))[0]
    values['alt']=struct.unpack('<I',f.read(4))[0]
    values['horiz1']=struct.unpack('<12H',f.read(24))
    values['horiz2']=struct.unpack('<12H',f.read(24))
    values['horizD']=struct.unpack('<12H',f.read(24))
    values['vert1']=struct.unpack('<12H',f.read(24))
    values['vert2']=struct.unpack('<12H',f.read(24))
    values['vertD']=struct.unpack('<12H',f.read(24))
    values['compassX']=struct.unpack('<12H',f.read(24))
    values['compassY']=struct.unpack('<12H',f.read(24))
    values['compassZ']=struct.unpack('<12H',f.read(24))
    values['cVert1']=struct.unpack('<15H',f.read(30))
    values['cVert2']=struct.unpack('<15H',f.read(30))
    values['sup']=struct.unpack('<4B',f.read(4))
    return values
	
def unpack_new(fstring):
    values={}
    values['version']=struct.unpack('<B',fstring[0:1])[0]
    values['yikes']=struct.unpack('<B',fstring[1:2])[0]
    values['seq']=struct.unpack('<H',fstring[2:4])[0]
    values['time']=struct.unpack('<I',fstring[4:8])[0]
    values['lat']=struct.unpack('<I',fstring[8:12])[0]
    values['lon']=struct.unpack('<I',fstring[12:16])[0]
    values['alt']=struct.unpack('<I',fstring[16:20])[0]
    values['horiz1']=struct.unpack('<12h',fstring[20:44])
    values['horiz2']=struct.unpack('<12h',fstring[44:68])
    values['horizD']=struct.unpack('<12h',fstring[68:92])
    values['vert1']=struct.unpack('<12h',fstring[92:116])
    values['vert2']=struct.unpack('<12h',fstring[116:140])
    values['vertD']=struct.unpack('<12h',fstring[140:164])
    values['compassX']=struct.unpack('<12h',fstring[164:188])
    values['compassY']=struct.unpack('<12h',fstring[188:212])
    values['compassZ']=struct.unpack('<12h',fstring[212:236])
    values['cVert1']=struct.unpack('<15h',fstring[236:266])
    values['cVert2']=struct.unpack('<15h',fstring[266:296])
    values['sup']=struct.unpack('<2H',fstring[296:300])
    values['ballast']=struct.unpack('<B',fstring[300:301])[0]
    values['cutdown']=struct.unpack('<B',fstring[301:302])[0]
    values['cond_time']=struct.unpack('<I',fstring[302:306])[0]

    return values
