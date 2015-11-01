import math
from graphics import *
from graphics import  _BBox
import random
import time
from win32con import NULL

#--[Global Constants]----------------------------------------------------------
SENSOR_TYPES = 2
MAX_LOCS = 25
MINX = 80
MINY = 80
MAXX = 400
MAXY = 400

#--[Class Arc]-----------------------------------------------------------------
# Extend Graphics.py to incorporate an arc
class Arc(_BBox):
    def __init__(self, center, radius, startAngle, extent):
        p1 = Point(center.x-radius, center.y-radius)
        p2 = Point(center.x+radius, center.y+radius)
        self.startAngle = startAngle
        self.extent = extent
        self.radius = radius
        _BBox.__init__(self, p1, p2)   
    
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
        
        ## [Opt] options details :-
        # opt can be following
        # start = starting angle in degrees
        # extent = spread of the arc in degrees
        # outline = the outline color of the arc
        # fill = fill color of the arc
        # style = tk.PIESLICE or tk.ARC or tk.CHORD 
        return canvas.create_arc((x1,y1,x2,y2),opt) 
     
#--[Class AreaOfInterest]------------------------------------------------------
# Represents the Rectangular Area of Interest
class AreaOfInterest:
    
    ## Lines forming the border of the rectangular region
    ## l1 is the left boundary and rest following in clockwise direction
    l1 = None
    l2 = None
    l3 = None
    l4 = None
    
    def __init__(self,l1,l2,l3,l4):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4
        
    
#--[Class Sensor ]-------------------------------------------------------------
## Represents a Sensor type
class Sensor:
    type = None
    range = None
    cost = None
    loc = None      # Set of feasible locations

    
    def __init__(self, typ, rg, cost,locs):
        self.s_type = typ
        self.s_range = rg
        self.s_cost = cost
        self.s_loc = locs
    

#--[Class Sensor Location ]-------------------------------------------------------------
## Represents a feasible location from the set of all feasible locations
# This will be used to represent properties associated with the sensor location
# like:-
# (a)  The sensor to which it belongs
# (b)  List of sensors whose sensing range overlaps the perimeter of the sensor
#      located at this location
#
# This class will be helpful to find perimeter overlaps by other sensors
class SensorLocation:
    
    def __init__ (self, point, sensor):
        
        self.point = point # The coordinate of the location
        self.sensor = sensor  # The sensor to which it belongs
        
        # List of sensors whose sensing range overlaps the perimeter of the 
        # sensor located at this location
        self.overlappingSensors = []    
    
    ## Adds a sensor to the list of overlapping sensors
    # @param sensorCenter: The center Point of the overlapping sensor
    # @param sensor: The object of the sensor class which is being added(i.e which is overalapping)
    # @param startAngle: The angle in degrees (measured anti-clockwise) at which the overlap starts with the perimeter of the sensor located at this location
    # @param endAngle: The angle in degrees (anti-clockwise) at which the overlap ends
    # @param extent: The extent of the overlap in degrees
    # @param distance: The eucildian distance between the centres of the overlapping sensor and this location
    def addOverlappingSensor(self,sensorCenter, sensor,startAngle, endAngle, extent, distance):
        self.overlappingSensors.append((sensorCenter, sensor, startAngle, endAngle, extent, distance) )
    

# Class to represent the circles which cover a portion of the perimeter of         
class CoveringCircle:
    def __init__(self, center, radius, s_ang, ext_ang, dist):
        self.center = center
        self.radius = radius
        self.s_angle = s_ang
        self.extent = ext_ang
        self.dist = dist
             
#--[Geometric Functions]-----------------------------------------------------------------
## distance(p1,p2)
#
# @param p1 : The first point
# @param p2 : The second point
#
# @return : The euclidian distance between two points

def distance(p1, p2):
    d = math.sqrt( (p2.x-p1.x) ** 2 + (p2.y - p1.y) ** 2 )
    return d

## flip(num)
#
# @param num : the input number
# 
# @return : the bit flipped number
def flip(num):
    return 1 ^ num

## sign(num)
#
# @param num : the input number whose sign has to be found out
# @return : -1 if the number is negetive else +1
def sign(num):
    return flip((num >> 31) & 0x1)

## Find the intersection of a line (defined by 2 points) and a circle (defined
# by a center_point and radius).
#
# @param cirlc: the input circle with whom intersection is to be found
# @param lineSeg: the input line segment with whom intersection is to be found
#
# @return :a tuple of the two intersecting points

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
        
        # Check if the point of intersection lies in within the line or not
        # (x1,y1) *------------#-----------------*(x2,y2)
        #                     (x,y)
        # if (x,y) is in between x1,y1 and x2,y2 then
        # x-x1 will be > 0 and x-x2 will be < 0, hence, their product < 0
        #
        # Similarly, 
        # y-y1 will be > 0 and y-y2 will be < 0, hence, their product < 0
        
        if ( ( (p1.x - x1) * (p1.x - x2) > 0) or ( (p1.y - y1) * (p1.y - y2) > 0)):
            p1 = None
        
        if ( ( (p2.x - x1) * (p2.x - x2) > 0) or ( (p2.y - y1) * (p2.y - y2) > 0)):
            p2 = None
        
        return (p1,p2)
    

## Find the distance of a point from a line
#
# @param c : The point from where the distance is to be calculated
# @param l : The line segment defined by two points
#
# @return : The euclidian distance between the line and the point
def pointLineDist(c, l):
    p1 = l.p1
    p2 = l.p2
    d = (p2.y - p1.y) * c.x - (p2.x - p1.x) * c.y + (p2.x * p1.y) - (p2.y * p1.x)
    d = d / math.sqrt( (p2.y - p1.y) ** 2 + (p2.x - p1.x) ** 2)
    return d
        
        
#--[Main Function]-------------------------------------------------------------
def main():
    # Given:
    #   Random locations of sensors
    #   Equal radius of all sensors
    #   Rectangular region to coverage
    
    
    sens = [] # Sensor object list
    locs = [] # SensorLocation object list 
    
#--[Sensor Types Attributes]---------------------------------------------------
    # 1. Range 
    Rs = [60,20,30,40,45,50,60,70,80,90]
    
    # 2. Cost
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
        
    
    win=GraphWin("Test Window", 500, 500)
    win.setCoords(0, 0, 500, 500)
    win.width=500
    win.height=500
    
    jr = Rectangle(Point(MINX, MINY),Point(MAXX, MAXY))
    jr.draw(win)
    
    
    t1 = time.time()
    
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