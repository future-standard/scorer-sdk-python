import sys,os
sys.path.append(os.pardir+"/libs")

import time
import DE_LIDAR

# Create a DE_LIDAR object
tof = DE_LIDAR.DE_LIDAR('/dev/ttyAMA0')

# Start ranging
tof.start_ranging()

distance = 0
while distance != tof.DE_LIDAR_TF02 :
    result = tof.get_distance()
    if tof.is_sig_success() :
        #print result
        distance = result['distance']
        if (distance == tof.DE_LIDAR_TF02) :
            # error distance == DE_LIDAR_TF02[22000]
            print ("error distance.")
        else :
            print ("%d cm" % (distance))
    time.sleep(0.01)

tof.stop_ranging()
