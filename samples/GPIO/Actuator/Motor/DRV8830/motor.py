import sys,os
sys.path.append(os.pardir)

import RPi.GPIO as GPIO
from libs import DRV8830
import time
import json
import sys

argvs = sys.argv
s = argvs[1];

result_json = {'status': 'OK','s':s}
print(json.dumps(result_json))

GPIO.setmode(GPIO.BCM)
motor = DRV8830.DRV8830(DRV8830.DRV8830_A1_A0_0_0)

motor.speed(int(s1))
time.sleep(5)

motor.clean()
GPIO.cleanup()
