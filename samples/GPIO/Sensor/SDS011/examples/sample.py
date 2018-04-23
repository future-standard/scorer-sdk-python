import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/libs")

import time
import SDS011
import json

sds011 = SDS011.SDS011('/dev/ttyUSB0')

sds011.begin()

result = sds011.read()
#sds011.sleep()
#sds011.wakeup()

sds011.end()

#status = result['status']
#pm25 = result['pm25']
#pm10 = result['pm10']

print(json.dumps(result))
#result_json = {'status':status,'pm25':pm25,'pm10':pm10}
#print(json.dumps(result_json))
