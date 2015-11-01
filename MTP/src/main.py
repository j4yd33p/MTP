import random
from graphics import *
import math


# Constants
SENSOR_TYPES = 10
MAX_LOCS = 10
MAXX = 200
MAXY = 200
XOFF = 0
YOFF = 0
## Hence the bounding rectangle = (0,0) - (200,200)

# List indexed by point
ptsHexList = [] # list of hexagons in whoose AOR this point lies
HexPtsList = [] # list of points indexed by hexagons


# Sensor Class
class Sensor:
    s_type=""
    s_range = 0
    s_cost = 0
    s_loc = []

    
    def __init__(self, typ, rg, cost,locs):
        self.s_type = typ
        self.s_range = rg
        self.s_cost = cost
        self.s_loc = locs
    
    
    
locs=[]
sens = [] # Sensor object list
#Sensor types attributes
#[Range]###
Rs = [2,3,5,7,7,10,15,20,30,40]

#[Cost]###
Cs = [1,1,1,1,1,1,1,1,1,1,1]

#[Locations]###
# Generate random coords of feasible sensor locations
for i in xrange(0,SENSOR_TYPES):
    for u in xrange(0,MAX_LOCS):
        locs.append( ( (random.random() * MAXX + XOFF), (random.random() * MAXY + YOFF) ) )

    sens.append(Sensor(i,Rs[i],Cs[i],locs) )


# Hexagon class -> Inherited from Polygon class of Graphics.py
class Hexagon(Polygon):
    
    center = Point(0,0)
    side = 0
    Epsilon = 0
    rMax = 0
    effAreaRect = []
    
    def __init__(self, center, rMax):
        self.center = center
        self.rMax = rMax
        self.side = 2 * rMax + self.Epsilon
        angle = 60 * math.pi / 180
    
        x = self.side * math.cos( angle) + center.x
        y = self.side * math.sin( angle) + center.y
        
        p1 = Point(x,y)
        #pList = [p1]
        pList = []
        
        for n in range(1,7):
            x = self.side * math.cos( n * angle) + center.x
            y = self.side * math.sin( n * angle) + center.y
            p2 = Point(x,y)
            pList.append(p2)
            
            p1 = p2
        
        # if points passed as a list, extract it
        Polygon.__init__(self,pList)
       
        
    def clone(self):
        return Polygon.clone(self)

    def getPoints(self):
        return Polygon.getPoints(self)

    def _move(self, dx, dy):
        Polygon._move(self,dx,dy)
   
    def _draw(self, canvas, options):
        return Polygon._draw(self,canvas,options)

    # contains: crossing number test for a point in a polygon
    #     Input:  P = Point object from graphics.py,
    #             V[] = vertex Points of a polygon
    #     Return: 0 = outside, 1 = inside
       
    def contains(self,P, V):
        cn = 0    # the crossing number counter
    
        # repeat the first vertex at end
        V = tuple(V[:])+(V[0],)
    
        # loop through all edges of the polygon
        for i in range(len(V)-1):   # edge from V[i] to V[i+1]
            if ((V[i].y <= P.y and V[i+1].y > P.y)   # an upward crossing
                or (V[i].y > P.y and V[i+1].y <= P.y)):  # a downward crossing
                # compute the actual edge-ray intersect x-coordinate
                vt = (P.y - V[i].y) / float(V[i+1].y - V[i].y)
                if P.x < V[i].x + vt * (V[i+1].x - V[i].x): # P[0] < intersect
                    cn += 1  # a valid crossing of y=P[1] right of P[0]
    
        return cn % 2   # 0 if even (out), and 1 if odd (in)

    # Effective area is the area of the Hexagon + area of the 6 x Rect of dimensions hex_side x rMax + the arcs at the corner with radius rMax
    # See the paper for more details
    def effectiveArea(self,win):
        ang = 30
        tmpLst = [] # temp list of points generated. From this we will generate the rectangle coords
        ihex = self
        
        for h in ihex.points:
            x = h.x + self.rMax * math.cos( ang * math.pi / 180)
            y = h.y + self.rMax * math.sin(ang * math.pi / 180)
            Line(h, Point(x,y)).draw(win)
            tmpLst.append(Point(x,y))
                    
            x = h.x + self.rMax * math.cos((ang+60) * math.pi / 180)
            y = h.y + self.rMax * math.sin((ang+60) * math.pi / 180)
            Line(h, Point(x,y)).draw(win)
            tmpLst.append(Point(x,y))
    
            ang += 60
        
        Circle(ihex.center,ihex.side + self.rMax).draw(win)
        self.effAreaRect = [
                   (ihex.points[0],ihex.points[1],tmpLst[2],tmpLst[1]),
                   (ihex.points[1],ihex.points[2],tmpLst[4],tmpLst[3]),
                   (ihex.points[2],ihex.points[3],tmpLst[6],tmpLst[5]),
                   (ihex.points[3],ihex.points[4],tmpLst[8],tmpLst[7]),
                   (ihex.points[4],ihex.points[5],tmpLst[10],tmpLst[9]),
                   (ihex.points[5],ihex.points[0],tmpLst[0],tmpLst[11])
                ]

    # Check if the point is in Hexagon
    # if not, then is it in any of the 6 rectangles
    # if not, then is it in the circle (this means if it is in any of the 6 sectors)
    def inEffectiveArea(self, tgtPoint):
        
        # Check if the point is in the hexagon
        r1=self.contains(tgtPoint, self.points)
        if(r1 == 1):
            print "Yes"
            return 1
        
        # check for containment in all the 6 rectangles
        for r in self.effAreaRect:
            r2 = self.contains(tgtPoint, r)
            if(r2 == 1):
                print "Yes"
                return 1
        
        #check inclusion in the circumcircle
        tgtDist = math.sqrt((tgtPoint.x - self.center.x) ** 2 + (tgtPoint.y - self.center.y) ** 2)
        
        return (tgtDist < (self.side + self.rMax))
    
     

class AreaOfInterest:
    
    hexTiles = []
    
    def __init__(self,hexTiles):
        self.hexTiles = hexTiles
    
    
    def hexTile(self,win,rect,hex_side):
        rect.draw(win)
        
        hexList = self.hexTiles
        
        xmin = rect.p1.x
        xmax = rect.p2.x
        
        ymin = rect.p1.y
        ymax = rect.p2.y
    
        x = xmin + hex_side / 2
        y = ymin - hex_side * math.sqrt(3) / 2 
        
        hex_ht = hex_side * math.sqrt(3)
        hex_width = 1.5 * hex_side
        
        vert_cnt = int(math.ceil((ymax-ymin) / hex_ht))
        horiz_cnt = int(math.ceil((xmax-xmin) / hex_width)) 
        
        for j in range (0,horiz_cnt):
            for i in range(0,vert_cnt):
                y += hex_side * math.sqrt(3)
                h = Hexagon(Point(x,y),hex_side)
                hexList.append(h)
                h.draw(win)
                            
            x += hex_side * math.sqrt(3) * math.cos(30 * math.pi/180)
            
            if (j % 2) == 0 :
                y = ymin - hex_side * math.sqrt(3)
            else:
                y =  ymin - hex_side * math.sqrt(3) / 2
        
        return hexList
            
            
# Plots the sensor's effective area. i.e the hexagon, 6 surrounding rectangles and the circumcircle    
def plotSensorArea(self,win,ihex,r):
        ang = 30
        tmpLst = [] # temp list of points generated. From this we will generate the rectangle coords
        
        for h in ihex.points:
            x = h.x + r * math.cos( ang * math.pi / 180)
            y = h.y + r * math.sin(ang * math.pi / 180)
            Line(h, Point(x,y)).draw(win)
            tmpLst.append(Point(x,y))
                    
            x = h.x + r * math.cos((ang+60) * math.pi / 180)
            y = h.y + r * math.sin((ang+60) * math.pi / 180)
            Line(h, Point(x,y)).draw(win)
            tmpLst.append(Point(x,y))
    
            ang += 60
        
        Circle(ihex.center,ihex.side+r).draw(win)
        rectLst = [
                   (ihex.points[0],ihex.points[1],tmpLst[2],tmpLst[1]),
                   (ihex.points[1],ihex.points[2],tmpLst[4],tmpLst[3]),
                   (ihex.points[2],ihex.points[3],tmpLst[6],tmpLst[5]),
                   (ihex.points[3],ihex.points[4],tmpLst[8],tmpLst[7]),
                   (ihex.points[4],ihex.points[5],tmpLst[10],tmpLst[9]),
                   (ihex.points[5],ihex.points[0],tmpLst[0],tmpLst[11])
                ]
        return rectLst     