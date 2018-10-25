#!/usr/bin/python

import serial
import re
import time

class VL53L1X_USB(object):
    """VL53L1X_USB ToF."""

    def __init__(self, port="/dev/ttyACM0", **kwargs):
        """Initialize the VL53L1X ToF Sensor from ST"""
        self.MAX = 4000
        self.serial = serial.Serial(port=port,
                        baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=10)

    def get_distance(self):
        self.result = {'distance':-1,'time':0,'max':self.MAX}
        if self.serial.in_waiting > 0 :
            v = re.split('[,\n]', self.serial.readline())
            if v[0] == '0':
                #print(v)
                """0,1958,3.68,5.44"""
                distance = -1
                t = 0.0
                if len(v) >= 6:
                    distance = int(v[2])
                    t = float(v[3])
                else :
                    distance = int(v[1])
                    t = float(v[2])
                self.result = {'distance':distance,'time':t,'max':self.MAX}
        return self.result

    def start_ranging(self):
        """start_ranging"""

    def stop_ranging(self):
        """stop_ranging"""
        self.serial.close()