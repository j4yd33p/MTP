import math
import graphics as gr
from jdgeometry import Point, Circle, Line, Polygon
import random
import time

#--[Class Set Cover]-----------------------------------------------------------
class SensorSet:
    
    __locs = []
    
    @property
    def locs(self):
        return self.__locs
    
    @locs.setter
    def locs(self,locList):
        self.__locs = locList
        
    def createSetCover(self,aoi,locsList):
        for i in range(len(locsList)):
            
            cov = aoi.isCoveredBy()
#--[End Class Set Cover]-------------------------------------------------------

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
    _flocs = None
    _sensList = None
    
    @property
    def sensList(self):
        return self._sensList
    
    @sensList.setter
    def sensList(self,sens):
        self._sensList = sens
    
    @property
    def flocs(self):
        return self._flocs
    
    @flocs.setter
    def flocs(self,locList):
        self._flocs = locList
        
    
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
    
    ## Function to calculate the perimeter coverage of all the sensors in the AOI
    # Uses private members as follows:-
    #     (a) self.flocs - the list of all feasible locations of all sensors
    #     (b) self.sensList - the list of all sensors of all sensor types
    #
    # @param indexSet: List of indices of locations and corresponding sensors to be checked
    #
    # Calculates the coverage of the perimeter of all sensors and saves it in a list associated with all sensors
    
    def calcPCL(self, indexSet):
    #--[Coverage Confirmation]-----------------------------------------------------
    
        locs = self.flocs
        sens = self.sensList
        
    # Find out all the semsors whose sensing circle has a portion outside the bounding rectangle
        ##(Start)#################################################
        for i in range(len(locs)):
            tempCircle = Circle(locs[i].point, locs[i].sensor.s_range)
    #         tempCircle.draw(win)
    #         win.getMouse()
            intPoints = tempCircle.intersection(self.rect)
            if len(intPoints) == 0 or intPoints == None :
                if sens[i].s_range >= self.diag/2:
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
                    if ( (self.l3.contains(intPoints[j]) and self.l3.contains(intPoints[j+1])) or\
                         (self.l2.contains(intPoints[j]) and self.l3.contains(intPoints[j+1]) ) or\
                         (self.l3.contains(intPoints[j]) and self.l4.contains(intPoints[j+1]) )):
                        
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
                
                d_ij = locs[i].point.distance(locs[j].point)
    
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
    # Check if the AOI is covered with the list of locations provided
    # @param locsIndexList : the list of indices of locations which form the set to be checked for coverage. 
    #                        They also index into the global sensor list
    # @return : True - if the AOI is covered by the input set
    #           False : otherwise
    
    def isCoveredBy(self,locsIndexList):
        # Sort overlaps in ascending order of starting angle

        locs = self.flocs
        sens = self.sensList
        
        areaNotCovered = False
        for i in locsIndexList:
            oSns = locs[i].overlappingSensors
            oSns.sort(key=lambda obj: obj[2])
            
#             for j in range(len(oSns)):
#                 print "(%f, %f)" % (oSns[j][2],oSns[j][3])
            # Check if the entire range of 0-360 deg is covered or not for each sensor
            prevAng = 0.0
            for j in range(0, len(oSns)):
                if oSns[j][2] > prevAng:    #oSns[j][2] = startingAngleOfOverlap
                    areaNotCovered = True
                    break;
                else:
                    if prevAng < oSns[j][3]:    # if the preAng is < endAngle, then
                        prevAng = oSns[j][3]    #oSns[j][2] = endingAngleOfOverlap
           
            if areaNotCovered:
                break

        if areaNotCovered:
            return False
        else:
            return True
    
#--[Class Sensor ]-------------------------------------------------------------
## Represents a Sensor type
class Sensor:
    type = None
    range = None
    cost = None
    loc = None      # Set of feasible locations
    curloc = None # index of the present location from the global list of locations

    
    def __init__(self, typ, rg, cost,locs,curloc):
        self.s_type = typ
        self.s_range = rg
        self.s_cost = cost
        self.s_loc = locs
        self.curloc = curloc
    

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