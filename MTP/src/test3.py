import math
from graphics import *
from graphics import  _BBox
import random
import time


# Constants
SENSOR_TYPES = 1
MAX_LOCS = 40
MINX = 80
MINY = 80
MAXX = 400
MAXY = 400
SENSOR_RADIUS = 65

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
        return canvas.create_arc((x1,y1,x2,y2),opt) #start = self.startAngle, extent = self.extent, outline='green'
     
        
class Angle:
    def __init__(self,ang,lr):
        self.angle = ang
        self.lr = lr # 0 = Left 1 = Right
        
        
class IntersectingCircle:
    def __init__(self, center, radius, s_ang, ext_ang, dist):
        self.center = center
        self.radius = radius
        self.s_angle = s_ang
        self.extent = ext_ang
        self.dist = dist
        
def distance(p1, p2):
    d = math.sqrt( (p2.x-p1.x) ** 2 + (p2.y - p1.y) ** 2 )
    return d

def main():
    # Given:
    #   Random locations of sensors
    #   Equal radius of all sensors
    #   Rectangular region to coverage
    
    locs = []
    near = []
    
    win=GraphWin("Test Window", 500, 500)
    win.setCoords(0, 0, 500, 500)
    win.width=500
    win.height=500
    
    jr = Rectangle(Point(MINX, MINY),Point(MAXX, MAXY))
    jr.draw(win)

#   
#     arc = Arc(Point(100,100), 2*SENSOR_RADIUS, 90, 10)
#     arc.draw(win)
               

#[Random Locations]####################################################
    # Generate random coords of feasible sensor locations
    for i in xrange(0,SENSOR_TYPES):
        for u in xrange(0,MAX_LOCS):
            pt = Point( (random.random() * (MAXX - MINX) + MINX), (random.random() * (MAXY - MINY) + MINY) )
            #sens = Circle(pt,SENSOR_RADIUS)
            #sens.draw(win) 
            locs.append (pt)
            
    t1 = time.time()
    
    for i in range(0, len(locs)):
        tmp = []
        for j in range (0,len(locs)):
            if (i == j):
                continue
            d_ij=distance(locs[i], locs[j])
            
            if(d_ij < 2 * SENSOR_RADIUS):
                y2 = locs[j].y
                x2 = locs[j].x
                y1 = locs[i].y
                x1 = locs[i].x
                
                slope = math.atan((y2-y1)/(x2-x1))
                
                ang = math.acos(d_ij / (2*SENSOR_RADIUS))
                
                # if the circle is in the southern hemisphere then the arc start and end angle change
                if(x2 > x1):
                    s_ang = slope - ang
                else:
                    s_ang = math.pi + slope - ang
                    
               
#                 o_al = Angle(al,0)
#                 o_ar = Angle(ar,1)
                iCir = IntersectingCircle(locs[j],SENSOR_RADIUS, s_ang, 2*ang ,d_ij)
                #win.getMouse()
                tmp.append(iCir)

        
            
                            
        near.append(tmp)
                        
    
    c=Circle(locs[0],SENSOR_RADIUS)
    c.draw(win)
    c.setOutline('red')
    
    for i in range(0,len(near)):
        for c in near[i]:
            s_ang = c.s_angle * 180 / math.pi
            ext = c.extent * 180 / math.pi
            
            Circle(c.center,c.radius).draw(win)
            arc = Arc(locs[i],c.radius, s_ang, ext)
            arc.draw(win,outline='blue',fill='red3',style='chord')
               
        #win.getMouse()
    
    t2 = time.time()
    print "Time spent = %d" % (t2-t1)
    win.getMouse()
    
    
    
    
main()