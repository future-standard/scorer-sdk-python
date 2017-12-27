import sys,os
sys.path.append(os.pardir)

import RPi.GPIO as GPIO 
from libs import DRV8833
import time
import json
import sys

argvs = sys.argv
s1 = argvs[1];
s2 = argvs[2];

result_json = {'status': 'OK','s1':s1,'s2':s2}
print(json.dumps(result_json))

GPIO.setmode(GPIO.BCM)
motorA = DRV8833.DRV8833(17,18)
motorB = DRV8833.DRV8833(22,23)

motorA.speed(int(s1))
motorB.speed(int(s2))
time.sleep(5)

motorA.clean()
motorB.clean()
GPIO.cleanup()
