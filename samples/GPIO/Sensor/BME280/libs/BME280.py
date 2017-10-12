"""
BME280

"""
import RPi.GPIO as GPIO
import smbus

BME280_ADDRESS    = 0x29

class BME280:
    """BME280"""
    def __init__(self, address=BME280_ADDRESS, i2c=None, **kwargs):
        """Initialize"""
