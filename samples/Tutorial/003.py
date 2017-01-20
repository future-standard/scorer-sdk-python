"""
 003.py

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

    # Get ROI data(Rectangle) from ROIStrage
    x1,y1,x2,y2 = roi.get_roi_rect_by_index(0)
    bgr = cv2.rectangle(bgr, (x1,y1),(x2,y2), (0,0,0), 1)

    # Show the original image to web
    scorer.imshow(1, bgr)

    # Trim the original image
    dst = bgr[y1:y2, x1:x2]

    # Convert to GRAY
    gray  = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)

    # Convert to BGR for overlay
    small = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Overlay the GRAY image to Original
    bgr[y1:y1+(y2-y1), x1:x1+(x2-x1)] = small

    # Show the result
    scorer.imshow(2, bgr)
