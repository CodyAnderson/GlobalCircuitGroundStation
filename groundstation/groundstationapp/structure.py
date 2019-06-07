import struct

PACKET_VERSION=3
def unpack(f):
    values={}
    values['version']=struct.unpack('<B',f.read(1))
    values['yikes']=struct.unpack('<B',f.read(1))
    values['seq']=struct.unpack('<H',f.read(2))
    values['time']=struct.unpack('<I',f.read(4))
    values['lat']=struct.unpack('<I',f.read(4))
    values['lon']=struct.unpack('<I',f.read(4))
    values['alt']=struct.unpack('<I',f.read(4))
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