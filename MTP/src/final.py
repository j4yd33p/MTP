from Sensors import *
import jdgeometry.geomfunctions as gf

#--[Global Constants]----------------------------------------------------------
SENSOR_TYPES = 5
MAX_LOCS = 6
MINX = 0
MINY = 0
MAXX = 400
MAXY = 400
AOI_P1 = Point(20,20) #Point(MINX+10, MINY+10)
AOI_P2 = Point(200,200) #Point(MAXX-10,MAXY-10)

        
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
# 1. We assume that there are inf sensors of each type
# 2. Hence, for our purpose, we generate those many sensors as many locations are generated
# 3. Each sensor generated will be of a particular type. Each sensor from the same type, thus, will have the same list of feasible locations
# 4. But, each sensor will also have the present location where it is placed currently
# 5. We assume that each location has a sensor and then compute min reqd sensors

    for i in xrange(0,SENSOR_TYPES):
        # temp list of locations for a specific sensor type
        sns_loc_set = []
         
        for u in xrange(0,MAX_LOCS):
             
            # genr a random point within the AOI
            pt = Point( (random.random() * (AOI_P2.x - AOI_P1.x) + AOI_P1.x), (random.random() * (AOI_P2.y - AOI_P1.y) + AOI_P1.y) )

            # Generate sensors with arbit Ranges and Costs
            sns = Sensor(i,Rs[i],Cs[i],None,None)
            
            # Append this genr pt to the set of feasibile locations for the Sensor Type i 
            sns_loc_set.append(pt)
            
            i_loc = SensorLocation(pt,sns) # Create a sensor loc object 
            
            # "locs" list is appended with the sensor placed at that loc. i.e the SensorLocation object  
            locs.append(i_loc)
            
            # Update the list of feasible locations for sns (the sensor object of type i). The feasible loc list will be same for all sensors
            # of the same sensor type
            sns.s_loc = sns_loc_set
            sns.curloc= len(locs) - 1 #The last index to which the present genr loc was added
            
            # Add the sensor generated to the list of sensors
            sens.append(sns)

#     j=0
#     
#     for i in xrange(0,SENSOR_TYPES):
#         sns_loc_set = []
#         
#         for u in xrange(0,MAX_LOCS):
#             
#             sns = Sensor(i,Rs[j],Cs[i],None) # Generate sensors with arbit Ranges and Costs
#             j= (j+1) % 10
# 
#             pt = Point( (random.random() * (AOI_P2.x - AOI_P1.x) + AOI_P1.x), (random.random() * (AOI_P2.y - AOI_P1.y) + AOI_P1.y) )
#             sns_loc_set.append(pt)
#             i_loc = SensorLocation(pt,sns)  
#             locs.append(i_loc)
#             sns.s_loc = sns_loc_set
#             sens.append(sns)


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
            print "(Prev, S, E) = (%f, %f, %f)" % (gf.toDeg(prevAng), gf.toDeg(oSns[j][2]), gf.toDeg(oSns[j][3]))
        
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
    

if __name__ == "__main__":
    main()
    