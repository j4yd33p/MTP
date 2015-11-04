import math
import graphics as gr
from jdgeometry import Point, Circle, Line, Polygon
import random
import time

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