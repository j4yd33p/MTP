import math
import graphics as gr
from sympy.geometry import *
import random
import time

# Constants
SENSOR_TYPES = 2
MAX_LOCS = 25
MINX = 80
MINY = 80
MAXX = 400
MAXY = 400

class SensorLocation:
    
    def __init__ (self, point, sensor):
        self.point = point
        self.sensor = sensor
        self.overlappingSensors = []
    
    def addOverlappingSensor(self,sensorCenter, sensor,startAngle, endAngle, extent, distance):
        self.overlappingSensors.append((sensorCenter, sensor, startAngle, endAngle, extent, distance) )
    
       
# Sensor Class
class Sensor:
    s_type=None
    s_range = None
    s_cost = None
    s_loc = []

    def __init__(self, typ, rg, cost,locs):
        self.s_type = typ
        self.s_range = rg
        self.s_cost = cost
        self.s_loc = locs
    
# Extend Graphics.py to draw an arc
class Arc(gr._BBox):
    def __init__(self, center, radius, startAngle, extent):
        p1 = Point(center.x-radius, center.y-radius)
        p2 = Point(center.x+radius, center.y+radius)
        self.startAngle = startAngle
        self.extent = extent
        self.radius = radius
        gr._BBox.__init__(self, p1, p2)   
    
    def clone(self):
        other = Arc(self.center, self.radius,self.startAngle,self.extent)
        other.config = self.config.copy()
        return other
   
    def draw(self, canvas, **options):
        p1 = self.p1
        p2 = self.p2
        opt = {'start':self.startAngle, 'extent':self.extent}
        opt.update(options)
        
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_arc((x1,y1,x2,y2),opt) #start = self.startAngle, extent = self.extent, outline='green'
     

# Class to represent the circles which cover a portion of the perimeter of         
class CoveringCircle:
    def __init__(self, center, radius, s_ang, ext_ang, dist):
        self.center = center
        self.radius = radius
        self.s_angle = s_ang
        self.extent = ext_ang
        self.dist = dist
        
def distance(p1, p2):
    d = math.sqrt( (p2.x-p1.x) ** 2 + (p2.y - p1.y) ** 2 )
    return d

def flip(num):
    return 1 ^ num

def sign(num):
    return flip((num >> 31) & 0x1)

def lineCircleIntersect(circle, lineSeg):
        x2 = lineSeg.p2.x
        y2 = lineSeg.p2.y
        x1 = lineSeg.p1.x
        y1 = lineSeg.p1.y
        r = circle.radius
        
        dx = x2 - x1
        dy = y2 - y1
        dr = math.sqrt(dx ** 2 + dy ** 2)
        
        D = x1*y2 - x2*y1
        
        tempNum2 = math.sqrt(r**2 * dr ** 2 - D ** 2)
        tempNum1 = sign(dy) * dx * tempNum2 
        tempDen1 = dr ** 2
        
        res_x1 = (D*dy + tempNum1) / tempDen1
        res_x2 = (D*dy - tempNum1) / tempDen1
        
        tempNum1 = abs(dy) * tempNum2      
        res_y1 = (-D*dx + abs(dy) * tempNum1)
        res_y2 = (-D*dx - abs(dy) * tempNum1)
        
        p1 = Point(res_x1, res_y1)
        p2 = Point(res_x2, res_y2)
        
        return (p1,p2)
        
def pointLineDist(c, p1, p2):
    d = (p2.y - p1.y) * c.x - (p2.x - p1.x) * c.y + (p2.x * p1.y) - (p2.y * p1.x)
    d = d / math.sqrt( (p2.y - p1.y) ** 2 + (p2.x - p1.x) ** 2)
    return d


def main():
    # Given:
    #   Random locations of sensors
    #   Equal radius of all sensors
    #   Rectangular region to coverage
    
    
    sens = [] # Sensor object list
    locs = [] # Locations which have a sensor associated with it ==> tuple(point, sensor_object)
    #Sensor types attributes
    #[Range]###
    Rs = [60,20,30,40,45,50,60,70,80,90]
    
    #[Cost]###
    Cs = [1,1,1,1,1,1,1,1,1,1,1]

#[Locations]###
# Generate random coords of feasible sensor locations
    j=0
    
    
    for i in xrange(0,SENSOR_TYPES):
        sns_loc_set = []
        
        for u in xrange(0,MAX_LOCS):
            
            sns = Sensor(i,Rs[j],Cs[i],None)
            j= (j+1) % 10
           
            
            pt = Point( (random.random() * (MAXX - MINX) + MINX), (random.random() * (MAXY - MINY) + MINY) )
            sns_loc_set.append(pt)
            i_loc = SensorLocation(pt,sns)
            locs.append(i_loc)
        
        sns.s_loc = sns_loc_set
        sens.append(sns)
        
    
    win=gr.GraphWin("Test Window", 500, 500)
    win.setCoords(0, 0, 500, 500)
    win.width=500
    win.height=500
    
    p1 = Point(MINX,MINY)
    p2 = Point(MINX,MAXY)
    p3 = Point(MAXX,MAXY)
    p4 = Point(MAXX,MINY)
    
    aoi = Polygon(p1,p2,p3,p4)
    pl = [gr.Point(p.x,p.y) for p in aoi.vertices]
    
    gr.Polygon(pl).draw(win)
    win.getMouse()
#   
#     arc = Arc(Point(100,100), 2*SENSOR_RADIUS, 90, 10)
#     arc.draw(win)
               
    t1 = time.time()
    
    
    for i in range(0,len(locs)):
        c1=Circle(locs[i].point, locs[i].sensor.s_range)
        isect = c1.intersection(aoi)
        if not isect:
           pass
        else:
            pass
            
             
    
    for i in range(0, len(locs)):
    
#         win.delete('all')
#         tempC = Circle(locs[i].point,locs[i].sensor.s_range)
#         tempC.setOutline('red')
#         tempC.draw(win)
        
#         locs[i].point.draw(win)
        
        for j in range (0,len(locs)):
            if (i == j):
                continue
            
            d_ij=distance(locs[i].point, locs[j].point)

#             Circle(locs[j].point,locs[j].sensor.s_range).draw(win)
#             locs[j].point.draw(win)
#             win.getMouse()
#--[Case 1]-------------------------------------------------------------------            
            # Case 1:- center of sensor j is out of the range of sensor i
            if(d_ij > locs[i].sensor.s_range):
                rj = locs[j].sensor.s_range
                ri = locs[i].sensor.s_range

                # if the distance between two sensors is < the sum of radii, 
                # then it means that there is some intersection                
                if( rj < (d_ij - ri) ):
                    continue
                
                if( (d_ij - ri) <= rj <= (d_ij + ri) ):
                # then the arc of si falling between [pi - a, pi + a] 
                # is perimeter covered by sj
                    cAng = (ri ** 2 + d_ij ** 2 - rj ** 2) / (2 * ri * d_ij)
                    ang = math.acos(cAng)

                    y2 = locs[j].point.y
                    x2 = locs[j].point.x
                    y1 = locs[i].point.y
                    x1 = locs[i].point.x
                    
                    slope = math.atan((y2-y1) / (x2-x1))
            
                    # if the circle is in the southern hemisphere then the arc start and end angle change
                    if(x2 > x1):
                        s_ang = slope - ang
                    else:
                        s_ang = math.pi + slope - ang
                    
                    e_ang = s_ang + 2 * ang
                    
#                     arc = Arc(locs[i].point,locs[i].sensor.s_range, (s_ang * 180/math.pi), 2*ang * 180/math.pi)
#                     arc.draw(win,outline='blue',fill='red3',style='chord')
#                     win.getMouse()
                    
                    locs[i].addOverlappingSensor( locs[j].point, locs[j].sensor, s_ang, e_ang, 2*ang, d_ij )
                    
                if ( rj > d_ij + ri):
                    # whole perimeter of sensor i is covered by sensor j
#                     arc = Arc(locs[i].point,locs[i].sensor.s_range, 0, 360)
#                     arc.draw(win,outline='blue',fill='red3',style='chord')
#                     win.getMouse()
                    locs[i].addOverlappingSensor( locs[j].point, locs[j].sensor, 0, 360, 360, d_ij )
                    
#--[Case 2]-------------------------------------------------------------------                    
            # Case 2:- center of sensor j is inside of the range of sensor i
            if(d_ij < locs[i].sensor.s_range):
                rj = locs[j].sensor.s_range
                ri = locs[i].sensor.s_range
                # if the distance between two sensors is < the sum of radii, 
                # then it means that there is some intersection                
                if( rj < (ri - d_ij) ):
                    continue
            
                if( (ri - d_ij ) <= rj <= (d_ij + ri) ):
                # then the arc of si falling between [pi - a, pi + a] 
                # is perimeter covered by sj
                    cAng = (ri ** 2 + d_ij ** 2 - rj ** 2) / (2 * ri * d_ij)
                    ang = math.acos(cAng)

                    y2 = locs[j].point.y
                    x2 = locs[j].point.x
                    y1 = locs[i].point.y
                    x1 = locs[i].point.x
                    
                    slope = math.atan((y2-y1)/(x2-x1))
            
                    # if the circle is in the southern hemisphere then the arc start and end angle change
                    if(x2 > x1):
                        s_ang = slope - ang
                    else:
                        s_ang = math.pi + slope - ang
                    
                    e_ang = s_ang + 2 * ang
                    
#                     arc = Arc(locs[i].point,locs[i].sensor.s_range, (s_ang * 180/math.pi), 2*ang * 180/math.pi)
#                     arc.draw(win,outline='blue',fill='red3',style='chord')
#                     win.getMouse()
                    locs[i].addOverlappingSensor( locs[j].point, locs[j].sensor, s_ang, e_ang, 2*ang , d_ij ) 
                    
                if ( rj > d_ij + ri):
                    # whole perimeter of sensor i is covered by sensor j
#                     arc = Arc(locs[i].point,locs[i].sensor.s_range, 0, 360)
#                     arc.draw(win,outline='blue',fill='red3',style='chord')
#                     win.getMouse()
                    locs[i].addOverlappingSensor( locs[j].point, locs[j].sensor, 0, 360, 360, d_ij ) 
                    
                    
#--[Print the Perimeter Covered Regions]----------------------------------------
    for i in range(0,len(locs)):
        sns = locs[i].sensor
        i_pt = locs[i].point
        
        for l_item in locs[i].overlappingSensors:
            j_pt = l_item[0]
            o_sns = l_item[1]
            s_angle = l_item[2]
            extent = l_item[4]
                 
            s_ang = s_angle * 180 / math.pi
            ext = extent * 180 / math.pi
            
            Circle(i_pt, sns.s_range).draw(win)
            arc = Arc(i_pt,sns.s_range, s_ang, ext)
            arc.draw(win,outline='blue',fill='red3',style='chord', activefill='blue')
               
        #win.getMouse()
    
    t2 = time.time()
    print "Time spent = %d" % (t2-t1)
    win.getMouse()
    
    
    
    
main()