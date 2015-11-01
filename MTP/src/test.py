from graphics import *
import random
import math

XORG = 100
YORG = 100
# Constants
SENSOR_TYPES = 10
MAX_LOCS = 10
MAXX = 200
MAXY = 200
XOFF = 0
YOFF = 0

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

    def contains (self,p): 
        q2x = abs(p.x - self.center.x)
        q2y = abs(p.y - self.center.y)
        _vert = self.side / 4
        _hori = self.side * math.sqrt(3)
        
        if (q2x > _hori) or (q2y > _vert*2) :
            return False         # bounding test (since q2 is in quadrant 2 only 2 tests are needed)

        return (2 * _vert * _hori - _vert * q2x - _hori * q2y) >= 0 # finally the dot product can be reduced to this due to the hexagon symmetry
    
    # Effective area is the area of the Hexagon + area of the 6 x Rect of dimensions hex_side x rMax + the arcs at the corner with radius rMax
    # See the paper for more details
    def effectiveArea(self,win):
        ang = 30
        tmpLst = [] # temp list of points generated. From this we will generate the rectangle coords
        ihex = self
        
        for h in ihex.points:
            x = h.x + self.rMax * math.cos( ang * math.pi / 180)
            y = h.y + self.rMax * math.sin(ang * math.pi / 180)
            #Line(h, Point(x,y)).draw(win)
            tmpLst.append(Point(x,y))
                    
            x = h.x + self.rMax * math.cos((ang+60) * math.pi / 180)
            y = h.y + self.rMax * math.sin((ang+60) * math.pi / 180)
            #Line(h, Point(x,y)).draw(win)
            tmpLst.append(Point(x,y))
    
            ang += 60
        
        #Circle(ihex.center,ihex.side + self.rMax).draw(win)
        self.effAreaRect = [
                   (ihex.points[0],ihex.points[1],tmpLst[2],tmpLst[1]),
                   (ihex.points[1],ihex.points[2],tmpLst[4],tmpLst[3]),
                   (ihex.points[2],ihex.points[3],tmpLst[6],tmpLst[5]),
                   (ihex.points[3],ihex.points[4],tmpLst[8],tmpLst[7]),
                   (ihex.points[4],ihex.points[5],tmpLst[10],tmpLst[9]),
                   (ihex.points[5],ihex.points[0],tmpLst[0],tmpLst[11])
                ]


    def drawEffectiveArea(self,win):
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
        r1=cn_PnPoly(tgtPoint, self.points)
        if(r1 == 1):
            print "Yes"
            return 1
        else:
            # check for containment in all the 6 rectangles
            for r in self.effAreaRect:
                r2 = cn_PnPoly(tgtPoint, r)
                if(r2 == 1):
                    print "Yes"
                    return 1
                else:
                    #check inclusion in the curcum-circle
                    tgtDist = math.sqrt((tgtPoint.x - self.center.x) ** 2 + (tgtPoint.y - self.center.y) ** 2)
        
        return (tgtDist < (self.side + self.rMax))
    
        
    
# [Hexagonal Tiling] 
# Tile a given rectangle with hexagons

def hexTile(win,rect,rMax):
    rect.draw(win)
    
    hexList = []
    hex_side = 2 * rMax
    
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
            h = Hexagon(Point(x,y),rMax)
            hexList.append(h)
            h.draw(win)

        x += hex_side * math.sqrt(3) * math.cos(30 * math.pi/180)
        
        if (j % 2) == 0 :
            y = ymin - hex_side * math.sqrt(3)
        else:
            y =  ymin - hex_side * math.sqrt(3) / 2
    
    return hexList


#===================================================================

# cn_PnPoly(): crossing number test for a point in a polygon
#     Input:  P = a point,
#             V[] = vertex points of a polygon
#     Return: 0 = outside, 1 = inside
# This code is patterned after [Franklin, 2000]

def cn_PnPoly(P, V):
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


def plotSquare(win, side):
    rect=Rectangle(Point(500/2-side//2,500/2-side//2), Point(500//2+side//2,500//2+side//2))

    rect.setWidth(5)
    rect.draw(win)

def plotCircle(win, radius, color):
    cir=Circle(Point(250,250), (radius))
    cir.setFill(color)
    cir.draw(win)

def plotHex(win, x0,y0,side):
    angle = 60 * math.pi / 180
    
    x = side * math.cos( angle) + x0
    y = side * math.sin( angle) + y0

    p1=Point(x,y)
    
    for n in range(1,8):
        x = side * math.cos( n * angle) + x0
        y = side * math.sin( n * angle) + y0
        p2 = Point(x,y)
        l = Line(p1,p2)
        l.draw(win)
        p1 = p2
        win.getMouse()
    

def plotPoints(win, side, pts):
    xoff=500/2-side//2
    yoff=500/2-side//2
    for i in range(0,pts):
        p1=Point(random.randint(0,side)+xoff, random.randint(0,side)+yoff)
        p1.draw(win)
        
# Draw the surrounding rectangles with side r, hex_side        
def plotSensorArea(win,ihex,r):
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

    


def main ():
    win=GraphWin("My Window", 500, 500)
    win.setCoords(0, 0, 500, 500)
    win.width=500
    win.height=500
    
    rMax = 40
    jr = Rectangle(Point(20,20),Point(400,300))
    #jr.draw(win)
    #h = Hexagon(Point(100,100),10)
    #h.effectiveArea(win)
    #h.draw(win)
    
    locs = []
    sens = [] # Sensor object list
    hexState = {}
    
    #Sensor types attributes
    #[Range]###
    Rs = [2,3,5,7,7,10,15,20,30,40]
    
    #[Cost]###
    Cs = [1,1,1,1,1,1,1,1,1,1,1]
    
    #[Locations]###
    # Generate random coords of feasible sensor locations
    for i in xrange(0,SENSOR_TYPES):
        for u in xrange(0,MAX_LOCS):
            locs.append( Point( (random.random() * MAXX + XOFF), (random.random() * MAXY + YOFF) ) )
    
    
    tes = hexTile(win, jr, rMax)
    
    for tst in locs:
        for tt in tes:
            tt.effectiveArea(win)
            yn = tt.inEffectiveArea(tst)
            if (yn == 1):
                if(hexState.has_key(tt)):
                    hexState[tt].append(tst)
                else:
                    hexState[tt] = [tst]
    

    hhh = hexState.keys()[3]
    hhh.drawEffectiveArea(win)
    Circle(hhh.center,5).draw(win)
    for xx in hexState[hhh]:
        xx.draw(win)
             
    #jrec = plotSensorArea(win, h, 20)
    win.getMouse()
    
    
#     win2 = GraphWin("Test",300,300)
#     win2.width=300
#     win2.height=300
#     
#     for i in range(0,len(jrec)):
#         Line(jrec[i][0],jrec[i][1]).draw(win2)
#         Line(jrec[i][1],jrec[i][2]).draw(win2)
#         Line(jrec[i][2],jrec[i][3]).draw(win2)
#         Line(jrec[i][3],jrec[i][0]).draw(win2)
#         
#     win2.getMouse()
    win.close



main()