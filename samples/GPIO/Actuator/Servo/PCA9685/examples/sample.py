import sys,os
sys.path.append(os.pardir)

from libs import PCA9685
import time

pwm = PCA9685.PCA9685(PCA9685.PCA9685_ADDRESS)
pwm.set_pwm_freq(60)

servo_min = 150
servo_max = 600

pwm.set_pwm(0, 0, servo_min)
time.sleep(1)

pwm.set_pwm(0, 0, servo_max)
time.sleep(1)

pwm.software_reset()
