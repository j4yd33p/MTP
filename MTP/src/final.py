import sys
sys.path.append('E:\\git_repos\\MTP\\MTP')
from Sensors import *
import jdgeometry.geomfunctions as gf

#--[Global Constants]----------------------------------------------------------
SENSOR_TYPES = 6
MAX_LOCS = 3
MINX = 0
MINY = 0
MAXX = 800
MAXY = 800
AOI_P1 = Point(20,20) #Point(MINX+10, MINY+10)
AOI_P2 = Point(420,520) #Point(MAXX-10,MAXY-10)
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
    Rs = [160,200,250,140,245,250,100,270,280,275]
    
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
    aoi.calcPCL(range(len(locs)))
    
    if aoi.isCoveredBy(range(len(locs))):
        print "Cov"
    else:
        print "Not Cov"
    
    
    for i in range(len(locs)):
        Circle(locs[i].point,locs[i].sensor.s_range).draw(win)
    
    win.getMouse()
    return
    #==[PCL Sort]=========================================
    # Sort the sensors as per their PCL
    # Map sens list to corresponding element in locs list
    # Sort this combination
    # Then split this combined list
    #=====================================================
    sens, locs = zip( *sorted(zip(sens,locs), key=lambda k: len(k[1].overlappingSensors)) )
    
    setcovers = []
    i=0
    for sj in range(len(sens)):
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
            setcovers[i] += (sj,)
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
    