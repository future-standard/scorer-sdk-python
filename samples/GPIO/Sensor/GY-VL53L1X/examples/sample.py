import sys,os
sys.path.append(os.pardir+"/libs")

import GY_VL53L1X
import time

tof = GY_VL53L1X.GY_VL53L1X("/dev/tty.usbserial-A901OBX1")
tof.write(GY_VL53L1X.LONG_DISTANCE_MEASUREMENT_MODE)

for c in range(0,100):
    result = tof.get_distance()
    print(result)
    time.sleep(0.1)

tof.stop_ranging()