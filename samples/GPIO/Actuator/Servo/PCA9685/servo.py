from libs import PCA9685
import json
import time
import sys

argvs = sys.argv
c = int(argvs[1]);
on = int(argvs[2]);
off = int(argvs[3]);

result_json = {'status': 'OK','c':c,'on':on,'off':off}
print(json.dumps(result_json))

pwm = PCA9685.PCA9685(PCA9685.PCA9685_ADDRESS)
pwm.set_pwm_freq(60)

pwm.set_pwm(c, on, off)
time.sleep(1)
