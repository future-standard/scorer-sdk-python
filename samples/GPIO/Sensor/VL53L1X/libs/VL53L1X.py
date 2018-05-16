#!/usr/bin/python

# https://github.com/sparkfun/SparkFun_VL53L1X_Arduino_Library/
# http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2

import time
from ctypes import *
import sys
import smbus

VL53L1_MAX_DISTANCE = 4000

I2C_BUFFER_LENGTH = 32

VL53L1_GPIO__TIO_HV_STATUS = 0x0031
VL53L1_SOFT_RESET = 0x0000
VL53L1_RESULT__FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0 = 0x0096

VL53L1_IDENTIFICATION__MODEL_ID = 0x010F
VL53L1_FIRMWARE__SYSTEM_STATUS = 0x00E5
VL53L1_PAD_I2C_HV__EXTSUP_CONFIG = 0x002E

configBlock = [
  0x29, 0x02, 0x10, 0x00, 0x28, 0xBC, 0x7A, 0x81, #8
  0x80, 0x07, 0x95, 0x00, 0xED, 0xFF, 0xF7, 0xFD, #16
  0x9E, 0x0E, 0x00, 0x10, 0x01, 0x00, 0x00, 0x00, #24
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x34, 0x00, #32
  0x28, 0x00, 0x0D, 0x0A, 0x00, 0x00, 0x00, 0x00, #40
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x11, #48
  0x02, 0x00, 0x02, 0x08, 0x00, 0x08, 0x10, 0x01, #56
  0x01, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x02, #64
  0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x0B, 0x00, #72
  0x00, 0x02, 0x0A, 0x21, 0x00, 0x00, 0x02, 0x00, #80
  0x00, 0x00, 0x00, 0xC8, 0x00, 0x00, 0x38, 0xFF, #88
  0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x91, 0x0F, #96
  0x00, 0xA5, 0x0D, 0x00, 0x80, 0x00, 0x0C, 0x08, #104
  0xB8, 0x00, 0x00, 0x00, 0x00, 0x0E, 0x10, 0x00, #112
  0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x0F, #120
  0x0D, 0x0E, 0x0E, 0x01, 0x00, 0x02, 0xC7, 0xFF, #128
  0x8B, 0x00, 0x00, 0x00, 0x01, 0x01, 0x40        #129 - 135 (0x81 - 0x87)
]

class VL53L1X(object):
    """VL53L1X ToF."""

    def __init__(self, address=0x29, **kwargs):
        """Initialize the VL53L1X ToF Sensor from ST"""
        self.device_address = address
        self._bus = smbus.SMBus(1)

    def start_ranging(self):
        """start_ranging"""
        #Check the device ID

        #i2cset -y 1 0x29 0x01 0x0f i
        #i2cget -y 1 0x29 0x01
        #i2cget -y 1 0x29 0x01
        modelID = self.readRegister16(VL53L1_IDENTIFICATION__MODEL_ID)
        #print ('modelID is {:04x}'.format(modelID))
        if (modelID != 0xEACC):
            return False

        self.softReset()

        """
        #i2cset -y 1 0x29 0x00 0xe5 i
        #i2cget -y 1 0x29 0x01
        #i2cget -y 1 0x29 0x01
        c=0
        v = (self.readRegister16(VL53L1_FIRMWARE__SYSTEM_STATUS) & 0x01)
        while (v == 0):
            print ("c %d v %04x" % (c,v))
            c+=1
            if (c == 100):
                return False
            time.sleep(1000/1000)
            v = (self.readRegister16(VL53L1_FIRMWARE__SYSTEM_STATUS) & 0x01)
        """

        result = self.readRegister16(VL53L1_PAD_I2C_HV__EXTSUP_CONFIG)
        result = (result & 0xFE) | 0x01
        #print ('result is {:04x}'.format(result))
        self.writeRegister16(VL53L1_PAD_I2C_HV__EXTSUP_CONFIG, result)
        return True

    def stop_ranging(self):
        """start_ranging"""

    def get_distance(self):
        """get_distance """
        #print ("get_distance")
        self.startMeasurement()
        #self.newDataReady()
        #while (self.newDataReady() == False):
        #    time.sleep(5/1000)
        distance = self.getDistance()
        #print ("distance %d" % (distance))
        return distance

    def get_max_distance(self):
        return VL53L1_MAX_DISTANCE

    def softReset(self):
        """Reset the sensor via software"""
        #i2cset -y 1 0x29 0x00 0x00 i
        #i2cset -y 1 0x29 0x00 0x01 i
        #i2cdump -y 1 0x29
        self.writeRegister(VL53L1_SOFT_RESET, 0x00) #Reset
        time.sleep(100/1000)
        self.writeRegister(VL53L1_SOFT_RESET, 0x01) #Exit reset
        time.sleep(100/1000)

    def startMeasurement(self):
        """Write a block of bytes to the sensor to configure it to take a measurement"""
        #print ("startMeasurement")
        address = 0x01
        leftToSend = len(configBlock)
        toSend = I2C_BUFFER_LENGTH - 2 #Max I2C buffer on Arduino is 32, and we need 2 bytes for address
        while (leftToSend > 0):
            if (toSend > leftToSend):
                toSend = leftToSend
            blocks = [address]
            for x in range(toSend):
                i = address + x - 1
                blocks.append(configBlock[i])
            #print('address %02x %d len %d' % (address, address, len(blocks)))
            #print(blocks)
            self._bus.write_i2c_block_data(self.device_address, 0x00, blocks)
            leftToSend -= toSend
            address += toSend

    def newDataReady(self):
        """Polls the measurement completion bit"""
        #i2cset -y 1 0x29 0x00 0x31 i
        #i2cget -y 1 0x29 0x00
        result = False
        v = self.readRegister(VL53L1_GPIO__TIO_HV_STATUS)
        #print ("newDataReady %02x" % (v))
        if(v != 0x03):
            result = True
        return result

    def getDistance(self):
        """Returns the results from the last measurement, distance in mm"""
        return (self.readRegister16(VL53L1_RESULT__FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0))

    def getSignalRate(self):
        """Returns the results from the last measurement, signal rate"""
        result = 0
        return result

    def getRangeStatus(self):
        """Returns the results from the last measurement, 0 = valid"""
        result = 0
        return result

    def readRegister(self, addr):
        """Reads one byte from a given location"""
        self._bus.write_byte_data(self.device_address, addr >> 8, addr & 0xFF)
        result = self._bus.read_byte_data(self.device_address,addr >> 8)
        #self._bus.write_byte_data(self.device_address,0x00,addr >> 8) #MSB
        #self._bus.write_byte_data(self.device_address,0x00,addr & 0xFF) #LSB
        #result = self._bus.read_byte_data(self.device_address,addr >> 8)
        return result

    def readRegister16(self, addr):
        """Reads two consecutive bytes from a given location"""
        self._bus.write_byte_data(self.device_address, addr >> 8, addr & 0xFF)
        msb = self._bus.read_byte_data(self.device_address,addr >> 8)
        lsb = self._bus.read_byte_data(self.device_address,addr >> 8)
        #self._bus.write_byte_data(self.device_address,0x00,addr >> 8) #MSB
        #self._bus.write_byte_data(self.device_address,0x00,addr & 0xFF) #LSB
        #msb = self._bus.read_byte_data(self.device_address,0x01)
        #lsb = self._bus.read_byte_data(self.device_address,0x01)
        result = (msb << 8 | lsb)
        #print ('result {:04x} {:02x} {:02x}'.format(result, msb, lsb))
        return result

    def writeRegister(self, addr, val):
        """Write a byte to a spot"""
        result = False
        self._bus.write_i2c_block_data(self.device_address,addr >> 8,[addr & 0xFF,val])
        result = True
        return result

    def writeRegister16(self, addr, val):
        """Write two bytes to a spot"""
        result = False
        self._bus.write_i2c_block_data(self.device_address,addr >> 8,[addr & 0xFF,val >> 8,val & 0xFF])
        result = True
        return result
