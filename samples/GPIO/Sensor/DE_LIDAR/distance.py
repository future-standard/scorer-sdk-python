import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/libs")

import time
import DE_LIDAR
import json

tof = DE_LIDAR.DE_LIDAR('/dev/ttyAMA0')

tof.start_ranging()

max_distance = tof.DE_LIDAR_TF02


distance = -1
status = 'NG'

while distance != tof.DE_LIDAR_TF02 :
    result = tof.get_distance()
    if tof.is_sig_success() :
        distance = result['distance']
        status = 'OK'
        break
  
result_json = {'status':status,'distance':distance,'max':max_distance}
print(json.dumps(result_json))

tof.stop_ranging()
