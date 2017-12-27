import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/libs")

import time
import VL53L0X
import json

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# VL53L0X 最長 2m 
max_distance = 2000

# 距離を取得してJSONで返却
timing = tof.get_timing()
if (timing < 20000): timing = 20000
distance = tof.get_distance()
if(max_distance < distance): distance = -1

result_json = {'status': 'OK','distance':distance,'max':max_distance,'timing':timing}
print(json.dumps(result_json))
tof.stop_ranging()
