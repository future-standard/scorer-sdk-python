#!/usr/bin/python3
"""
 image_judgement.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""
import signal
import os
import sys
import cv2
import time
import scorer
import RPi.GPIO as GPIO

# Home Directory
home = os.environ['HOME']

# Signal Handler
def closing_func(num, frame):
    print("Singal Catched.")
    GPIO.output(24, 0)
    GPIO.output(23, 0)
    GPIO.cleanup()

signal.signal(signal.SIGINT,  closing_func)
signal.signal(signal.SIGTERM, closing_func)

# GPIO Set UP
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

# Threshold for templete matiching
Threshold=0.93

# Template matching method
method = cv2.TM_CCORR_NORMED

# Capture Interval (Sec)
interval = 15

# Uploader
uploader = scorer.Uploader("RPIMAGAZINE")

# Get Capture Image
cap = scorer.VideoCapture(0)

img_list = []

timer_started=False
while True:
    # Get Frame from Camera
    frame = cap.read()
    if frame == None:
        sys.exit()
    
    # Get BGR and Gray image
    bgr = frame.get_bgr()
    img_b, img_g, img_r = cv2.split(bgr)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
   
    # Get target image
    template1 = cv2.imread(home + '/scorer-sdk-python/samples/Raspi-Magazine/image/target.png',1)
    template1_b, template1_g, template1_r = cv2.split(template1)
    template1 = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
    
    # Apply Template matching
    res1 = cv2.matchTemplate(gray,template1,method)
    res1_b = cv2.matchTemplate(img_b,template1,method)
    res1_g = cv2.matchTemplate(img_g,template1,method)
    res1_r = cv2.matchTemplate(img_r,template1,method)
    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
    min_val1_b, max_val1_b, min_loc1_b, max_loc1_b = cv2.minMaxLoc(res1_b)
    min_val1_g, max_val1_g, min_loc1_g, max_loc1_g = cv2.minMaxLoc(res1_g)
    min_val1_r, max_val1_r, min_loc1_r, max_loc1_r = cv2.minMaxLoc(res1_r)
    val1=(max_val1)*(max_val1_b)*(max_val1_g)*(max_val1_r)

    ### For Debug
    print("max_val1=%e, max_val1_b=%e, max_val1_g=%e, max_val1_r=%e" % (max_val1,max_val1_b,max_val1_g,max_val1_r))
    print("max val1 ",val1)
   
    if val1 >= Threshold:
        print("Recording")
        GPIO.output(24, 0)
        GPIO.output(23, 1)
    
        # Timer    
        if timer_started == False:
            print("Timer Started")
            start_time=time.mktime(time.localtime())
            timer_started = True
            continue
  
        # Check Interval 
        now=time.mktime(time.localtime()) 
        if timer_started == True and now-start_time >= interval:
            # Image Upload
            img_list.append(bgr)

            # Upload to SMC
            if uploader.upload(images= img_list) == False:
                    print("upload failed.")
            print("uploader succeeded.")
            del img_list[:]

            # Timer Reset
            timer_started=False
            start_time=time.mktime(time.localtime())
            print("Capture Recoreded")
    else:
        print("Stop")
        GPIO.output(24, 1)
        GPIO.output(23, 0)
        timer_started=False

