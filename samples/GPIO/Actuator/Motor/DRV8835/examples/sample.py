import sys,os
sys.path.append(os.pardir)

import RPi.GPIO as GPIO
from libs import DRV8835
import time

GPIO.setmode(GPIO.BCM)
motorA = DRV8835.DRV8835(17,18)
motorB = DRV8835.DRV8835(22,23)

for i in range(-100,100,25):
    motorA.speed(i)
    print('motorA {0}'.format(i))
    time.sleep(1)

motorA.brake()
print('motorA brake')

for i in range(-100,100,25):
    motorB.speed(i)
    print('motorB {0}'.format(i))
    time.sleep(1)

motorB.brake()
print('motorB brake')

motorA.clean()
motorB.clean()
GPIO.cleanup()
