#!/usr/bin/python3
"""
 saveimg.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""
import cv2
import sys
import os
import scorer
import RPi.GPIO as GPIO
from time import sleep

# Import Scorer Library for ROI
sys.path.append("../lib")
import scorer_util

args = sys.argv

# GPIO Set UP
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
pin_list=(24,23)

# Get ROI Information
roi = scorer_util.ROIStorage(os.path.dirname(__file__)+"/raspi_magazine.json")
x1,y1,x2,y2 = roi.get_roi_rect_by_index(0)

# Get Camera Object
cap = scorer.VideoCapture(0)

if len(args) >1:
    # Get Image Frame
    frame = cap.read()
    if frame == None:
        sys.exit()
   
    # Get BGR data(CvMati format) 
    bgr = frame.get_bgr()
 
    # Trim the BGR Image
    rect = bgr[y1:y2, x1:x2]

    if args[1] == "on":
        # Save the Image
        cv2.imwrite("image/target.png",rect)

        # GPIO Operation
        for i in range(5):
            GPIO.output(pin_list, 1)
            sleep(0.2)
            GPIO.output(pin_list, 0)
            sleep(0.2)
        GPIO.cleanup()

        print("target saved")
    
