import math
import graphics as gr
from jdgeometry import Point, Circle, Line, Polygon
import random
import time

#--[Global Constants]----------------------------------------------------------
SENSOR_TYPES = 5
MAX_LOCS = 6
MINX = 0
MINY = 0
MAXX = 400
MAXY = 400
AOI_P1 = Point(20,20) #Point(MINX+10, MINY+10)
AOI_P2 = Point(200,200) #Point(MAXX-10,MAXY-10)


     
#--[Class AreaOfInterest]------------------------------------------------------
# Represents the Rectangular Area of Interest
class AreaOfInterest:
    
    ## Lines forming the border of the rectangular region
    ## l1 is the left boundary and rest following in clockwise direction
    l1 = None
    l2 = None
    l3 = None
    l4 = None
    rect = None
    diag = None
    
    def __init__(self,l1,l2,l3,l4):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4
        self.rect = Polygon(l1.p1, l2.p1, l3.p1, l4.p1)
        self.diag = l1.p1.distance(l2.p2)
    
    @classmethod
    def byDiagonal(cls,p1,p2):
        l1 = Line(p1, Point(p1.x, p2.y))
        l2 = Line(Point(p1.x,p2.y), p2)
        l3 = Line(p2, Point(p2.x, p1.y))
        l4 = Line(Point(p2.x,p1.y), p1)
    
        return cls(l1,l2,l3,l4)
    
    
    @classmethod
    def byLine(cls,l1, l2, l3, l4):
        return cls(l1,l2,l3,l4)
    
    
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
        # Tuple:    (thisSensorCenter, 
        #            overlapping_sensor_object, 
        #            startAngleOfOverlap, 
        #            endAngleOfOverlap, 
        #            extent, 
        #            distanceBetweenSensors )
        self.overlappingSensors = []    
    
    ## Adds a sensor to the list of overlapping sensors
    # @param sensorCenter: The center Point of the overlapping sensor
    # @param sensor: The object of the sensor class which is being added(i.e which is overalapping)
    # @param startAngle: The angle in degrees (measured anti-clockwise) at which the overlap starts with the perimeter of the sensor located at this location
    # @param endAngle: The angle in degrees (anti-clockwise) at which the overlap ends
    # @param extent: The extent of the overlap in degrees
    # @param distance: The eucildian distance between the centres of the overlapping sensor and this location
    def addOverlappingSensor(self,sensorCenter, sensor,startAngle, endAngle, extent, distance):

        
        normal = False
        if startAngle < 0:
            e1 = 2*math.pi + startAngle
            self.overlappingSensors.append((sensorCenter, sensor, e1, 2*math.pi, e1, distance) )
            self.overlappingSensors.append((sensorCenter, sensor, 0, endAngle, extent - e1, distance) )
            normal = False
        else:
            normal = True
            
        if endAngle > 2 * math.pi:
            e1 = 2*math.pi - startAngle
            self.overlappingSensors.append((sensorCenter, sensor, startAngle, 2*math.pi, e1, distance) )
            self.overlappingSensors.append((sensorCenter, sensor, 0, (endAngle - 2*math.pi), extent - e1, distance) )
            normal = False
        else:
            normal = True
        
        if normal == True:
            self.overlappingSensors.append((sensorCenter, sensor, startAngle, endAngle, extent, distance) )

# Class to represent the circles which cover a portion of the perimeter of         
class CoveringCircle:
    def __init__(self, center, radius, s_ang, ext_ang, dist):
        self.center = center
        self.radius = radius
        self.s_angle = s_ang
        self.extent = ext_ang
        self.dist = dist
        
#--[Class Arc]-----------------------------------------------------------------
# Extend Graphics.py to incorporate an arc
class Arc(gr._BBox):
    def __init__(self, center, radius, startAngle, extent):
        p1 = gr.Point(center.x-radius, center.y-radius)
        p2 = gr.Point(center.x+radius, center.y+radius)
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
        
        ## [Opt] options details :-
        # opt can be following
        # start = starting angle in degrees
        # extent = spread of the arc in degrees
        # outline = the outline color of the arc
        # fill = fill color of the arc
        # style = tk.PIESLICE or tk.ARC or tk.CHORD 
        return canvas.create_arc((x1,y1,x2,y2),opt)         
         
#--[Geometric Functions]-----------------------------------------------------------------

## Convert Radians to Degrees
# @param rad: angle in radians
#
# @return : Angle in degrees
def toDeg(rad):
    return rad * 180.0 / math.pi

## Convert Degrees to Radians
# @param rad: angle in degrees
#
# @return : Angle in radians
def toRad(deg):
    return deg * math.pi / 180.0

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

#--[Generate Locations]--------------------------------------------------------
# Generate random coords of feasible sensor locations
    j=0
    
    for i in xrange(0,SENSOR_TYPES):
        sns_loc_set = []
        
        for u in xrange(0,MAX_LOCS):
            
            sns = Sensor(i,Rs[j],Cs[i],None) # Generate sensors with arbit Ranges and Costs
            j= (j+1) % 10
           
            
            pt = Point( (random.random() * (AOI_P2.x - AOI_P1.x) + AOI_P1.x), (random.random() * (AOI_P2.y - AOI_P1.y) + AOI_P1.y) )
            sns_loc_set.append(pt)
            i_loc = SensorLocation(pt,sns)  
            locs.append(i_loc)
            sns.s_loc = sns_loc_set
            sens.append(sns)
##############################################################################        
    
    # Create Window canvas where sensors will be displayed
    ######################
    win=gr.GraphWin("Test Window", MAXX, MAXY)
    win.setCoords(MINX, MINY, MAXX, MAXY)
    win.width=MAXX - MINX
    win.height=MAXY - MINY
    
    aoi = AreaOfInterest.byDiagonal(AOI_P1,AOI_P2)
    
    
    jr = aoi.rect
    jr.draw(win)
    
    ########################
    
    t1 = time.time()
#--[Coverage Confirmation]-----------------------------------------------------

# Find out all the semsors whose sensing circle has a portion outside the bounding rectangle
    ##(Start)#################################################
    for i in range(0,len(locs)):
        tempCircle = Circle(locs[i].point, locs[i].sensor.s_range)
#         tempCircle.draw(win)
#         win.getMouse()
        intPoints = tempCircle.intersection(aoi.rect)
        if len(intPoints) == 0 or intPoints == None :
            if sens[i].s_range >= aoi.diag/2:
                locs[i].addOverlappingSensor( None, None, 0, 2*math.pi, 2*math.pi, 0 )
            
            continue
        else:
            for j in range(0, len(intPoints), 2):   # Check two intersection points at a time
                
                # line from the center to the intersection points of length sensor_range
                l1 = Line(locs[i].point, intPoints[j])
                l2 = Line(locs[i].point, intPoints[j+1])
                
                # Center location of the sensor
                cx = locs[i].point.x
                cy = locs[i].point.y

                # x,y coords of the intersection points
                x1 = intPoints[j].x
                x2 = intPoints[j+1].x
                y1 = intPoints[j].y
                y2 = intPoints[j+1].y
                
                # Find the angle of the arc formed by the two points
                l1_ang = math.atan(l1.slope) 
                l2_ang = math.atan(l2.slope)
                
                 
                if (x1 <= cx and y1 <= cy) or (x1 <= cx and y1 >= cy): # this means the line lies in 2nd or 3rd quadrant
                    l1_ang = l1_ang + math.pi
                if (x1 >= cx and y1 <= cy): # this means the line lies in 1st or 4th quadrant
                    l1_ang = l1_ang +  2 * math.pi

                if (x2 <= cx and y2 <= cy) or (x2 <= cx and y2 >= cy): # this means the line lies in 2nd or 3rd quadrant
                    l2_ang = l2_ang + math.pi
                if (x2 >= cx and y2 <= cy): # this means the line lies in 1st or 4th quadrant
                    l2_ang = l2_ang + 2 * math.pi
                    
                # The angle of the sector formed by the two intersection points
                ang = abs(l1_ang - l2_ang)
                
                # Check if the sensor range cuts the right most boundary of the aoi
                if ( (aoi.l3.contains(intPoints[j]) and aoi.l3.contains(intPoints[j+1])) or\
                     (aoi.l2.contains(intPoints[j]) and aoi.l3.contains(intPoints[j+1]) ) or\
                     (aoi.l3.contains(intPoints[j]) and aoi.l4.contains(intPoints[j+1]) )):
                    
                    if (l1_ang > l2_ang):
                        s_ang = l1_ang
                        ang = 2*math.pi - l1_ang + l2_ang
                    else:
                        s_ang = l2_ang
                        ang = 2*math.pi - l2_ang + l1_ang
                else:
                    if (l1_ang < l2_ang):
                        s_ang = l1_ang
                    else:
                        s_ang = l2_ang
                    
                e_ang = s_ang + ang
                extent = ang * 180/math.pi
                
                
                locs[i].addOverlappingSensor( None, None, s_ang, e_ang, ang, 0 )
#                 gr.Circle(locs[i].point,locs[i].sensor.s_range).draw(win)
#                 Arc(locs[i].point,locs[i].sensor.s_range,s_ang * 180/math.pi,extent).draw(win,outline='red',style='pieslice')
#                 win.getMouse()

    ##(End)####################################################3
        
    for i in range(0, len(locs)):
#         win.delete('all')
#         Circle(locs[i].point, sens[i].s_range).draw(win,outline='red')
#         Circle(locs[i].point,1).draw(win)
#         aoi.rect.draw(win)
        
        for j in range (0,len(locs)):
            if (i == j):
                continue
            
#             Circle(locs[j].point, sens[j].s_range).draw(win)
#             win.getMouse()
            
            d_ij = distance(locs[i].point, locs[j].point)

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
                    
                    if slope < 0:
                        if x2 < x1:
                            slope += math.pi
                        if y2 < y1:
                            slope += math.pi * 2
                    else:
                        if x2 < x1 and y2 < y1:
                            slope += math.pi    
                    # if the circle is in the southern hemisphere then the arc start and end angle change
#                     if(x2 > x1):
#                         s_ang = slope - ang
#                     else:
#                         s_ang = math.pi + slope - ang
                    s_ang = slope - ang
                    e_ang = s_ang + 2 * ang
                 
                    locs[i].addOverlappingSensor( locs[j].point, locs[j].sensor, s_ang, e_ang, 2*ang, d_ij )
                    
                if ( rj > d_ij + ri):
                    # whole perimeter of sensor i is covered by sensor j
                    locs[i].addOverlappingSensor( locs[j].point, locs[j].sensor, 0, 2*math.pi, 360, d_ij )
                    
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
            
                    if slope < 0:
                        if x2 < x1:
                            slope += math.pi
                        if y2 < y1:
                            slope += math.pi * 2
                    else:
                        if x2 < x1 and y2 < y1:
                            slope += math.pi  
                    # if the circle is in the southern hemisphere then the arc start and end angle change
#                     if(x2 > x1):
#                         s_ang = slope - ang
#                     else:
#                         s_ang = math.pi + slope - ang
                    
                    s_ang = slope - ang
                    e_ang = s_ang + 2 * ang
                    
                    locs[i].addOverlappingSensor( locs[j].point, locs[j].sensor, s_ang, e_ang, 2*ang , d_ij ) 
                    
                if ( rj > d_ij + ri):
                    # whole perimeter of sensor i is covered by sensor j
                    locs[i].addOverlappingSensor( locs[j].point, locs[j].sensor, 0, 2*math.pi, 360, d_ij ) 
                    

#--[Angular Coverage]--------------------------------------------
    # Sort overlaps in ascending order of starting angle
    
    areaNotCovered = False
    for i in range(0,len(locs)):
        oSns = locs[i].overlappingSensors
        print "Sensor id=%d-----------------------------" % i
        oSns.sort(key=lambda obj: obj[2])
        
        for j in range(len(oSns)):
            print "(%f, %f)" % (oSns[j][2],oSns[j][3])
        # Check if the entire range of 0-360 deg is covered or not for each sensor
        prevAng = 0.0
        for j in range(0, len(oSns)):
            if oSns[j][2] > prevAng:    #oSns[j][2] = startingAngleOfOverlap
                Circle(locs[i].point,sens[i].s_range).draw(win,outline='blue')
                print "Area not covered (prevEnd, start, end)=(%f,%f,%f)" % (prevAng, oSns[j][2],oSns[j][3])
                areaNotCovered = True
                break;
            else:
                if prevAng < oSns[j][3]:    # if the preAng is < endAngle, then
                    prevAng = oSns[j][3]    #oSns[j][2] = endingAngleOfOverlap
            print "(Prev, S, E) = (%f, %f, %f)" % (toDeg(prevAng), toDeg(oSns[j][2]), toDeg(oSns[j][3]))
        
        if areaNotCovered:
            break
########################################################
                    
#--[Print the Perimeter Covered Regions]----------------------------------------
#     win.getMouse()
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
#             arc = Arc(i_pt,sns.s_range, s_ang, ext)
#             arc.draw(win,outline='blue',style='chord', activefill='blue')
               
        #win.getMouse()
    
    t2 = time.time()
    print "Time spent = %d" % (t2-t1)
    win.getMouse()
    
    
    
    
main()    