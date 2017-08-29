import json
import sys
import os
import scorer

sys.path.append("../lib")
import scorer_util

roi = scorer_util.ROIStorage(os.path.dirname(__file__)+"/thermo.json")

count = roi.get_roi_rect_len()
for i in range(count):
    x1,y1,x2,y2 = roi.get_roi_rect_by_index(i)
    print(x1)
    print(y1)
    print(x2)
    print(y2)
