import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/libs")

import SDS011
import json

sds011 = SDS011.SDS011('/dev/ttyUSB0')

sds011.begin()

result = sds011.read()
#status = result['status']
#pm25 = result['pm25']
#pm10 = result['pm10']

#sds011.sleep()
#sds011.wakeup()

sds011.end()

#result_json = {'status':status,'pm25':pm25,'pm10':pm10}
print(json.dumps(result))
