"""
DRV8835 デュアルモータードライバ 1.5A

"""
import RPi.GPIO as GPIO
import time

class DRV8835:
    def __init__(self,in1,in2):
        """ DRV8835 """
        self.in1 = in1
        self.in2 = in2

        GPIO.setup(in1, GPIO.OUT)
        GPIO.output(in1,False)
        self.in1Pwm = GPIO.PWM(in1,20*1000) #20kHz
        self.in1Pwm.start(0)

        GPIO.setup(in2, GPIO.OUT)
        self.in2Pwm = GPIO.PWM(in2,20*1000) #20kHz
        self.in2Pwm.start(0)

    def speed(self,speed):
        """ speed """
        if (speed < 0):
            GPIO.output(self.in1,False)
            self.in2Pwm.ChangeDutyCycle(abs(speed))
        else :
            self.in1Pwm.ChangeDutyCycle(abs(speed))
            GPIO.output(self.in2,False)
        
        
    def brake(self):
        """ brake """
        GPIO.output(self.in1,False)
        GPIO.output(self.in2,False)
        self.in1Pwm.ChangeDutyCycle(0)
        self.in2Pwm.ChangeDutyCycle(0)

    def clean(self):
        """ clean """
        GPIO.output(self.in1,False)
        GPIO.output(self.in2,False)
        self.in1Pwm.stop()
        self.in2Pwm.stop()