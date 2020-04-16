import dxfgrabber

import sys
import math
import glob


def getXY(point):
    x, y = point[0], point[1]
    return x,y


listfile=glob.glob("*.dxf")
f= open("output.csv","w+")
f.write("file;length\n")
for filepath in listfile:
    dxf = dxfgrabber.readfile(filepath)
    shapes = dxf.entities.get_entities()

    dist=0

    for shape in shapes:
        if shape.dxftype == 'LINE':
            x1, y1 = getXY(shape.start)
            x2, y2 = getXY(shape.end)
            dist = dist+ math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
        elif shape.dxftype== 'POLYLINE' or shape.dxftype== 'LWPOLYLINE':
            first_point=shape.points[0]
            point1=first_point
            first=True
            for point2 in shape.points:
                if(first==False):
                    x1,y1=getXY(point1)
                    x2,y2=getXY(point2)
                    dist = dist+math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
                    point1=point2
                first=False
            x1,y1=getXY(first_point)
            x2,y2=getXY(point2)
                
            dist = dist+math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
            
        
            
        elif shape.dxftype == 'ARC':
             dist = dist+(math.pi*shape.radius*2) * ((shape.end_angle-shape.start_angle)/360)
           
    f.write(filepath+";"+str(dist)+"\n")
    print (filepath+" => "+str(dist))
f.close()
