"""
 factory_demo.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""
import cv2
import sys
import numpy as np
import scorer

# import module for ROIStrage
sys.path.append("../lib")
import scorer_util

cnt=0

args = sys.argv
if len(args) > 1:
	thresh = int(args[1])
else:
	thresh = 50

cap = scorer.VideoCapture(0)
roi = scorer_util.ROIStorage()

while True:
	frame = cap.read()
	if frame == None:
		continue

	bgr = frame.get_bgr()

	x1,y1,x2,y2 = roi.get_roi_rect_by_index(0)
	width = int(x2-x1)
	height = int(y2-y1)
	ret ,binary_img = cv2.threshold(bgr, thresh, 255, cv2.THRESH_BINARY)
	crop_img = binary_img[y1:y2, x1:x2]
	m = int(np.count_nonzero(crop_img))
	m = int((width*height*3-m)*100/(width*height*3))
	bgr = cv2.rectangle(bgr, (x1,y1), (x2,y2), (0,0,255), 3)
	scorer.imshow(1,bgr)
	scorer.imshow(2,crop_img)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	cnt = cnt + 1
	if cnt % 1 == 0:
		print(str(m)+"%")

