import sys,os
sys.path.append(os.pardir+"/libs")

import time
import VL53L1X_USB
tof1 = VL53L1X_USB.VL53L1X_USB("/dev/ttyACM0")
#tof2 = VL53L1X_USB.VL53L1X_USB("/dev/ttyACM1")

# Start ranging
for c in range(0,100):
    result1 = tof1.get_distance()
    print(result1)
    #print ("tof1 %d %d mm" % (c, result1['distance']))
    #result2 = tof2.get_distance()
    #print ("tof2 %d %d mm" % (c, result2['distance']))
    time.sleep(0.3)

tof1.stop_ranging()
#tof2.stop_ranging()
