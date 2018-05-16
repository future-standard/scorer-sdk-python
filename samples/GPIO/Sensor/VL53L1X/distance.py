import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/libs")

import time
import VL53L1X
import json

tof = VL53L1X.VL53L1X()

tof.start_ranging()

avg = 0
c = 0
for r in range(0,100):
    d = tof.get_distance()
    if(d > 0):
        avg += d
        c += 1

distance = 0
if (c > 0):
    distance = int(avg/c)
result_json = {'status': 'OK','distance':distance,'max':tof.get_max_distance()}
print(json.dumps(result_json))

tof.stop_ranging()
