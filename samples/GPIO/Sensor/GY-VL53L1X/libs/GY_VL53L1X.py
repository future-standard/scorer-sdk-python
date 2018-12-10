#!/usr/bin/python

import serial
import time

CONTINUOUS_OUTPUT_DISTANCE = [0xA5,0x45,0xEA]
QUERY_OUTPUT_DISTANCE_DATA = [0xA5,0x15,0xBA]

SAVE_THE_CONFIGURATION = [0xA5,0x25,0xCA]

LONG_DISTANCE_MEASUREMENT_MODE  = [0xA5,0x50,0xF5]
FAST_MEASUREMENT_MODE           = [0xA5,0x51,0xF6]
HIGH_PRECISION_MEASUREMENT_MODE = [0xA5,0x52,0xF7]
GENERAL_MEASUREMENT_MODE        = [0xA5,0x53,0xF8]

class GY_VL53L1X(object):
    """VL53L1X+STM32 ToF."""

    def __init__(self, port="/dev/ttyACM0", **kwargs):
        self.MAX = 4000
        self.PORT = port
        self.serial = serial.Serial(port=self.PORT,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=10)

    def get_distance(self):
        self.result = {'distance':-1,'max':self.MAX}
        #print ("in_waiting %d" % (self.serial.in_waiting))
        if self.serial.in_waiting > 0 :
            for c in range(0,self.serial.in_waiting):
                #print "---"
                v = self.serial.read()
                if ord(v) == 0x5A:
                    v = self.serial.read()
                    if ord(v) == 0x5A:
                        v = self.serial.read()
                        if ord(v) == 0x15:
                            v = self.serial.read()
                            if ord(v) == 0x03:
                                v = self.serial.read(3)
                                distance = (v[0]) << 8 | (v[1])
                                #python2
                                #distance = ord(v[0]) << 8 | ord(v[1])
                                #mode = ord(v[2])
                                #print ("distance %d mm, mode %d" % (distance,mode))
                                self.result = {'distance':distance,'max':self.MAX}
                                break
        return self.result

    def start_ranging(self):
        """start_ranging"""

    def stop_ranging(self):
        """stop_ranging"""
        self.serial.close()

    def write(self,v):
        # CONTINUOUS_OUTPUT_DISTANCE
        # QUERY_OUTPUT_DISTANCE_DATA
        self.serial.write(v)
