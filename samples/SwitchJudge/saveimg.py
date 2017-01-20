import cv2
import sys
import os
import scorer

sys.path.append("../lib")
import scorer_util

args = sys.argv

cap = scorer.VideoCapture(0)
roi = scorer_util.ROIStorage(os.path.dirname(__file__)+"/switchjudge.json")

x1,y1,x2,y2 = roi.get_roi_rect_by_index(0)

if len(args) >1:
    frame = cap.read()
    if frame == None:
        sys.exit()
    
    bgr = frame.get_bgr()
    rect = bgr[y1:y2, x1:x2]

    if args[1] == "on":
        #cv2.imwrite("/opt/scorer/home/dev/scorer-python/on.png",rect)
        cv2.imwrite("image/on.png",rect)
        print("on saved")
    
    elif args[1] == "off":
        cv2.imwrite("image/off.png",rect)
        print("off saved")

