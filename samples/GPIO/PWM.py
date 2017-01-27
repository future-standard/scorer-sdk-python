"""
 PWM.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""
import time
import os
import RPi.GPIO as GPIO            # import RPi.GPIO module  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output   
p24 = GPIO.PWM(24, 60)
p24.start(0)
try:
    while True:
        # Gradually brighter
        for dc in range(0, 101, 20):
            p24.ChangeDutyCycle(dc)
            time.sleep(0.1)


        # Gradually darken
        for dc in range(100, -1, -20):
            p24.ChangeDutyCycle(dc)
            time.sleep(0.1)

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    p24.stop()
    GPIO.cleanup()  
