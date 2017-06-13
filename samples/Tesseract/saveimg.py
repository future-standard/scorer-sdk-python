#!/usr/bin/env python3
import cv2
import sys
import os
import scorer

sys.path.append("../lib")
import scorer_util

args = sys.argv

TARGET_DIR = "./image/"
if not os.path.isdir(TARGET_DIR):
    os.makedirs(TARGET_DIR)

cap = scorer.VideoCapture(0)
roi = scorer_util.ROIStorage(os.path.dirname(__file__)+"/tesseract.json")

x1,y1,x2,y2 = roi.get_roi_rect_by_index(0)

frame = cap.read()
if frame == None:
    sys.exit(1)
    
bgr = frame.get_bgr()
rect = bgr[y1:y2, x1:x2]

cv2.imwrite("image/tesseract.bmp",rect)
os._exit(0)

