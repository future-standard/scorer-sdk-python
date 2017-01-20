"""
 002.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""
import scorer
import sys
import cv2

# import module for ROIStrage
sys.path.append("../lib")
import scorer_util

# Setup VideoCaputre Object
cap = scorer.VideoCapture(0)

# Read ROI data
roi = scorer_util.ROIStorage()

while True:
    # Read Frame from Camera
    frame = cap.read()
    if frame == None:
       continue

    # Convert the Frame to BGR
    bgr = frame.get_bgr()

    # Show the image to Web
    scorer.imshow(1, bgr)

    # Get ROI data(Circle) from ROIStrage
    for i in range(roi.get_roi_circle_len()):
        x,y,radius = roi.get_roi_circle_by_index(i)
        bgr = cv2.circle(bgr, (x,y), radius, (0,0,255), 5)

    # Get ROI data(Line) from ROIStrage
    for i in range(roi.get_roi_line_len()):
        x1,y1,x2,y2 = roi.get_roi_line_by_index(i)
        bgr = cv2.line(bgr, (x1,y1),(x2,y2), (255,0,0), 5)

    # Get ROI data(Rectangle) from ROIStrage
    for i in range(roi.get_roi_rect_len()):
        x1,y1,x2,y2 = roi.get_roi_rect_by_index(i)
        bgr = cv2.rectangle(bgr, (x1,y1),(x2,y2), (0,255,0), 5)

    # Show the image with ROI data to Web
    scorer.imshow(2, bgr)
