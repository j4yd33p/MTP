import math
import numpy
from graphics import *
 

def arcArea(startAngle, endAngle, radius, chordLen):

    theta = math.acos((radius**2 + radius**2 - chordLen**2)/(2*radius**2))
    area = 1/2 * (theta - math.sin(theta)) * radius**2
    
    return area

def sign(num):
    return flip((num >> 31) & 0x1)


def flip(num):
    return 1 ^ num

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
        
    