import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/libs")

import time
import HR168
import json

hr168 = HR168.HR168('/dev/ttyUSB0')

hr168.start_ranging()
distance = "-1"
status = 'NG'

result = hr168.get_distance()
distance = result['distance']
if distance != "-1" :
    status = 'OK'

result_json = {'status':status,'distance':distance,'max':hr168.MAX_DISTANCE}
print(json.dumps(result_json))

hr168.stop_ranging()
