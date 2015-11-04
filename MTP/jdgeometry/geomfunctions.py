import math
from jdgeometry import Point
     
        
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
        