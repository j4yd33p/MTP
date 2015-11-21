import sys
sys.path.append('E:\\git_repos\\MTP\\MTP')
from Sensors import *
import jdgeometry.geomfunctions as gf

#--[Global Constants]----------------------------------------------------------
SENSOR_TYPES = 5
MAX_LOCS = 5
MINX = 0
MINY = 0
MAXX = 400
MAXY = 400
AOI_P1 = Point(20,20) #Point(MINX+10, MINY+10)
AOI_P2 = Point(200,200) #Point(MAXX-10,MAXY-10)
## Scale used is 1pixel = 10 km on ground
        
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
    #Rs = [160,200,250,140,245,250,100,270,280,275]
    #Rs = [50,25,45,30,37,42,27,43,40,30]
    Rs = [60,20,50,40,65,50,60,70,80,90]
    # 2. Cost
    Cs = [1,1,1,1,1,1,1,1,1,1,1]

    #tstPts = [(320,470), (400,370), (320,250), (200,370)]
    tstPts = [(46.2181988653702, 78.9937201939627),
(88.5585724310382, 62.9228371547380),
(156.569807744921, 77.1317153041696),
(75.5410578299005, 129.791564721792),
(145.062223358807, 128.790793916331),
(97.6349437712055, 179.381492390987),
(22.3118968187630, 60.8137549727227),
(112.941625669823, 66.0284721752555),
(189.817555686223, 162.729027054340),
(40.0092183351116, 24.7681775390030),
(190.209055587435, 98.2389192564382),
(41.6335420376567, 51.3036808407277),
(141.843012283537, 87.9865270641189),
(198.172370280841, 105.365594316510),
(28.7950830364038, 154.211191664831),
(135.276784728651, 116.423763724089),
(184.889945255442, 83.1060916064103),
(164.305535952445, 120.688636336573),
(196.558421318560, 57.4354930176322),
(131.175729299857, 27.9577177461996),
(81.1059489645708, 43.6057223648023),
(90.9533323505153, 58.1073883587396),
(149.657865128203, 34.9648586446983),
(185.246424752466, 70.4145112463445),
(72.7991840589153, 26.4581797243417),
(65.7335491231121, 185.508023128886),
(148.044436262498, 184.750010369155),
(73.1343948280671, 95.2370271259956),
(107.236623008858, 139.149553300860),
(154.587922530711, 50.0700573328505)]
    
    jIdxSet = list((0, 6, 9, 11, 14, 10, 25, 18, 5, 13, 26, 7, 23, 24, 16, 19, 20, 21, 22, 3, 17, 0, 29, 28, 1, 4))
    #jIdxSet = list((29, 2, 15, 12, 4, 1, 28, 29, 0, 17, 3, 22, 21, 20, 19, 16, 24, 23, 7, 26, 13, 5, 18, 25, 10, 14, 11, 9, 6))
                   
    #jIdxSet = list((29, 2, 15, 12, 4, 1, 28, 29, 0, 17, 3, 22, 21, 20, 19, 16, 24))
    
#--[Generate Locations]--------------------------------------------------------
# Generate random coords of feasible sensor locations
# 1. We assume that there are inf sensors of each type
# 2. Hence, for our purpose, we generate those many sensors as many locations are generated
# 3. Each sensor generated will be of a particular type. Each sensor from the same type, thus, will have the same list of feasible locations
# 4. But, each sensor will also have the present location where it is placed currently
# 5. We assume that each location has a sensor and then compute min reqd sensors

    j=0
    for i in xrange(0,SENSOR_TYPES):
        # temp list of locations for a specific sensor type
        sns_loc_set = []
         
        for u in xrange(0,MAX_LOCS):
             
            # genr a random point within the AOI
            #pt = Point( (random.random() * (AOI_P2.x - AOI_P1.x) + AOI_P1.x), (random.random() * (AOI_P2.y - AOI_P1.y) + AOI_P1.y) )
            pt = Point( tstPts[j])
            j += 1

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

    
    # Copy of the location list. This will help in finding the overlapping 
    # sensors as Sensor class keeps the index of location to which it is assigned
    locsCopy = locs[:]
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
    
    aoi.flocs = locs
    aoi.sensList = sens
    
    jr = aoi.rect
    jr.draw(win)
    
    ########################
    
    t1 = time.time()

#==[Find Set Covers]=======================================================
# Sort the sensors as per the PCL values in non-decreasing order
# Use greedy strategy and calculate set covers
# Check coverage level of each cover
#==========================================================================
    
# Find the PCL for each sensor
    aoi._win = win
#     aoi.calcPCL(range(len(locs)))
    
    if aoi.isCoveredBy(range(len(locs))):
        print "Cov"
    else:
        print "Not Cov"
        #return
#         
#     for u in jIdxSet:
#         p = locsCopy[u].point
#         s = locsCopy[u].sensor
#         Circle(p,s.s_range).draw(win)
#        
#     win.getMouse()
#     return
       
      
    
#     sens, locs = zip( *sorted(zip(sens,locs), key=lambda k: k[1].overlappingCount) )
     
#     for i in range(len(locs)):
#         Circle(locs[i].point,locs[i].sensor.s_range).draw(win)
#         print "I = %i, ol = %d" % (i, locs[i].overlappingCount)
#     
#     win.delete("all")
#     idx = len(locs) - 1
#     Circle(locs[idx].point,locs[idx].sensor.s_range).draw(win,outline="red")
#     jc=0
#     for i in range (len(locs[idx].overlappingSensors)):
#         s = locs[idx].overlappingSensors[i][1]
#         jc += 1
#         if s != None :
#             p = locsCopy[s.curloc].point
#             p.draw(win)
#             Circle(p, s.s_range).draw(win,outline="blue")
#             win.getMouse()
#             p.undraw()
#              
#     print jc
#     return


    #==[PCL Sort]=========================================
    # Sort the sensors as per their PCL
    # Map sens list to corresponding element in locs list
    # Sort this combination
    # Then split this combined list
    #=====================================================
    sens, locs = zip( *sorted(zip(sens,locs), key=lambda k: k[1].overlappingCount) )
    
    setcovers = []
    i=0
    for sj in range(len(sens)-1,-1,-1):
        # Check if the ith set cover exists or not
        if len(setcovers) <= i : # if the length = the present index, means last valid indexs is (length - 1) 
            # ith set cover doesnt exist
            setcovers.append((sj,))
            print "Creating cover %d" % i
            continue

        print "I=%d" % i
        print setcovers[i]
        is_covered = aoi.isCoveredBy(setcovers[i])
        
        if not is_covered:
            # if this set doesnt cover the AOI, then append another sensor to this set
            setcovers[i] += (locs[sj].sensor.curloc,)
        else:
            # if the set of sensors covers the AOI, then create the next cover
            i = i + 1
    
##[End Set Covers]#############################################################
                    
#--[Print the Perimeter Covered Regions]----------------------------------------

    for i in setcovers[0]: #range(len(locs)):
        sns =  locs[i].sensor
        i_pt = locs[i].point
        
        Circle(i_pt, sns.s_range).draw(win)
    
    t2 = time.time()
    print "Time spent = %d" % (t2-t1)
    win.getMouse()


if __name__ == "__main__":
    main()
    