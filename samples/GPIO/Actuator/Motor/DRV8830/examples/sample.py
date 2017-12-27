import sys,os
sys.path.append(os.pardir)

import RPi.GPIO as GPIO
from libs import DRV8830
import time

GPIO.setmode(GPIO.BCM)
motor = DRV8830.DRV8830(DRV8830.DRV8830_A1_A0_0_0)

for i in range(-100,100,25):
    motor.speed(i)
    print('motor {0}'.format(i))
    time.sleep(1)

motor.brake()
print('motor brake')

motor.clean()
GPIO.cleanup()
