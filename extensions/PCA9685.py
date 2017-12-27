"""
Adafruit_Python_PCA9685を参考に作成
https://github.com/adafruit/Adafruit_Python_PCA9685

"""

import RPi.GPIO as GPIO            # import RPi.GPIO module  
import time  
import smbus
import math

PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01

PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04
SWRST              = 0x06

class PCA9685:
    """PCA9685"""
    
    def __init__(self, address=PCA9685_ADDRESS, **kwargs):
        """Initialize"""
        self._address = address
        self._bus = smbus.SMBus(1)
        self._bus.write_byte_data(self._address, 0x00, 0x00)
        self._bus.write_byte_data(self._address,MODE2, OUTDRV)
        self._bus.write_byte_data(self._address,MODE1, ALLCALL)
        time.sleep(0.005)
        mode1 = self._bus.read_byte_data(self._address, MODE1)
        mode1 = mode1 & ~SLEEP  # wake up (reset sleep)
        self._bus.write_byte_data(self._address,MODE1, mode1)
        time.sleep(0.005)  # wait for oscillator
        
    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        prescale = int(math.floor(prescaleval + 0.5))
        oldmode = self._bus.read_byte_data(self._address,MODE1);
        self.newmode = (oldmode & 0x7F) | 0x10    # sleep
        self._bus.write_byte_data(self._address, MODE1, self.newmode)  # go to sleep
        self._bus.write_byte_data(self._address, PRESCALE, prescale)
        self._bus.write_byte_data(self._address, MODE1, oldmode)
        time.sleep(0.005)
        self._bus.write_byte_data(self._address, MODE1, oldmode | 0x80)
        
    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        self._bus.write_byte_data(self._address, LED0_ON_L+4*channel, on & 0xFF)
        self._bus.write_byte_data(self._address, LED0_ON_H+4*channel, on >> 8)
        self._bus.write_byte_data(self._address, LED0_OFF_L+4*channel, off & 0xFF)
        self._bus.write_byte_data(self._address, LED0_OFF_H+4*channel, off >> 8)
        
    def software_reset(self):
        """ software_reset """
        bus = smbus.SMBus(1)
        bus.write_byte_data(self._address, 0x00, self.newmode)