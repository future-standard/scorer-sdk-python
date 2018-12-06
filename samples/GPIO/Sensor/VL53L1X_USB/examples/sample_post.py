import sys,os
sys.path.append(os.pardir+"/libs")

import requests
import time
import VL53L1X_USB
tof1 = VL53L1X_USB.VL53L1X_USB("/dev/ttyACM0")
# Start ranging
for c in range(0,100):
    result1 = tof1.get_distance()
    headers = {'Content-type': 'application/json'}
    r = requests.post("https://us-central1-vl53l1x-usb.cloudfunctions.net/tof", headers=headers, json=result1)
    print(r.status_code, r.reason, r.text)
    time.sleep(0.3)

tof1.stop_ranging()
