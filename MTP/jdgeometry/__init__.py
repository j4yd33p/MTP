import graphics as gr
import sympy.geometry as geom

class Point(geom.Point):
    def draw(self,canvas, **options):
        self.obj = gr.Point(self.x, self.y)
        if options.has_key('outline'):
            self.obj.setOutline(options['outline'])
        
        self.obj.draw(canvas)
        
class Circle (geom.Circle):
    def draw(self,canvas, **options):
        self.obj = gr.Circle(gr.Point(self.center.x, self.center.y),self.radius)
        if options.has_key('outline'):
            self.obj.setOutline(options['outline'])
        self.obj.draw(canvas)

class Ellipse(geom.Ellipse):
    def __init__(self,center, hradius, vradius, eccentricity):
        geom.Ellipse.__new__(center, hradius, vradius, eccentricity)
        p1 = Point(center.x-hradius, center.y-vradius)
        p2 = Point(center.x+hradius, center.y+vradius)
        gr.Oval.__init__(self, p1, p2)

    def draw(self,canvas, *options):
        p1 = gr.Point(self.center.x - self.hradius, self.center.y - self.vradius)
        p2 = gr.Point(self.center.x + self.hradius, self.center.y + self.vradius)
        self.obj = gr.Oval(p1,p2)
        self.obj.draw(canvas,*options)
        
class Line(geom.Line):
    def draw(self,canvas, *options):
        p1 = gr.Point(self.p1.x,self.p1.y)
        p2 = gr.Point(self.p2.x,self.p2.y)
        self.obj = gr.Line(p1,p2)
        self.obj.draw(canvas,*options)

class Polygon(geom.Polygon):
    def draw(self,canvas, *options):
        _ptList = [gr.Point(p.x,p.y) for p in self.vertices]
        self.obj = gr.Polygon(_ptList)
        self.obj.draw(canvas,*options)
        
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
