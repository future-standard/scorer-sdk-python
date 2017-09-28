#!/usr/bin/python
"""
 readAR.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""

import sys
import os
import subprocess
import cv2
import scorer

argv = sys.argv
argc = len(argv)

if (argc != 2):
    print ('Usage: python %s <intrinsic yml>' % argv[0])
    exit()

TARGET_DIR = os.path.abspath(os.path.dirname(__file__)) + "/image"
if not os.path.isdir(TARGET_DIR):
    os.makedirs(TARGET_DIR)


cmd = os.path.abspath(os.path.dirname(__file__)) + "/readAR"
yml = argv[1]
img = os.path.abspath(os.path.dirname(__file__)) + "/image/aruco.jpg"
log = os.path.abspath(os.path.dirname(__file__)) + "/log.txt"

cap = scorer.VideoCapture(0)
frame = cap.read()
bgr = frame.get_bgr()
cv2.imwrite(img,bgr)

if os.path.exists(yml):
    if os.path.exists(img):
        ret = subprocess.check_output([cmd, yml, img, log])
        print(ret.decode('utf-8'))
    else:
        print (img + ' does not exist')
        exit()
else:
    print (yml + ' does not exist')
    exit()
