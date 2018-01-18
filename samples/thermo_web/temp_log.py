#!/usr/bin/env python3

import scorer
import json
from time import sleep
import cv2
import sys
import os

sys.path.append("../lib")
import scorer_util

print(os.path.dirname(__file__) + "\n")
roi = scorer_util.ROIStorage(os.path.dirname(__file__)+"/thermo.json")

# Interval for log output
INTERVAL=10 # Sec

# Image upload flag
IMAGE_UPLOAD=False

IMAGE_FNAME="tempimg.jpg"

# Uploader
uploader = scorer.Uploader("TERMO_CAMERA")
sleep(5)

img_list = []

# Get ROI
roi_array=[]
count = roi.get_roi_rect_len()
for i in range(count):
    x1,y1,x2,y2 = roi.get_roi_rect_by_index(i)
    local_roi=[x1, y1, x2, y2]
    roi_array.append(local_roi)

while True:

    if IMAGE_UPLOAD==True:
        img = cv2.imread(IMAGE_FNAME)
        img_list.append(img)

    try:
        f = open('tempdata.json', 'r')
    except FileNotFoundError:
        sleep(10)
        continue

    try:
        jsonData = json.load(f)
    except Exception:
        sleep(10)
        continue

    stable = "Stable" if jsonData["Stable"] == "true" else "Unstable"


    log_string = stable + "," + "Whole,max:" + jsonData["Whole"]["max"] + ",min:" + jsonData["Whole"]["min"] + ",avg:" + jsonData["Whole"]["avg"]

    num=len(jsonData["ROI"])
    for i in range(num):
        name="Rect" + str(i)
        log_string = log_string + "," + name + ",x1:" + str(roi_array[i][0]) + ",y1:" + str(roi_array[i][1]) + ",x2:" + str(roi_array[i][2]) + ",y2:" + str(roi_array[i][3]) + ",max:" + jsonData["ROI"][name]["max"] + ",min:" + jsonData["ROI"][name]["min"] + ",avg:" + jsonData["ROI"][name]["avg"]

    print(log_string)

    # Upload to SMC
    if IMAGE_UPLOAD==True:
        if uploader.upload(log_str= log_string, images = img_list) == False:
            print("upload failed.")
        del img_list[:]
    else:
        if uploader.upload(log_str= log_string) == False:
            print("upload failed.")

    sleep(INTERVAL)
