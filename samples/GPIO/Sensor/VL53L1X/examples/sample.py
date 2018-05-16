import sys,os
sys.path.append(os.pardir+"/libs")

import time
import VL53L1X
tof = VL53L1X.VL53L1X()

# Start ranging
result = tof.start_ranging()
if(result == True):
    for c in range(0,100):
        distance = tof.get_distance()
        print ("%d %d mm" % (c, distance))
        time.sleep(10/1000)

tof.stop_ranging()
