"""
DRV8830 I2cモータードライバ

"""
import RPi.GPIO as GPIO
import time

DRV8830_A1_A0_0_0       = 0x60
DRV8830_A1_A0_0_OPEN    = 0x61
DRV8830_A1_A0_OPEN_0    = 0x62
DRV8830_A1_A0_OPEN_OPEN = 0x63
DRV8830_A1_A0_OPEN_1    = 0x64
DRV8830_A1_A0_1_0       = 0x65
DRV8830_A1_A0_1_OPEN    = 0x66
DRV8830_A1_A0_1_1       = 0x67

class DRV8830:
    def __init__(self,addr):
        """ DRV8830 """
        self._address = address
        self._bus = smbus.SMBus(1)
        self._bus.write_byte_data(self._address, 0x00, 0x00)
    def speed(self,speed):
        """ speed """
        power = 0x00
        if (speed < 0):
            power |= 0x01
        else :
            power |= 0x02
        self._bus.write_byte_data(self._address, 0x00, power)

    def brake(self):
        """ brake """
        self._bus.write_byte_data(self._address, 0x00, 0x03)

    def clean(self):
        """ clean """
        self._bus.write_byte_data(self._address, 0x00, 0x00)
        self._bus.write_byte_data(self._address, 0x01, 0x80)
