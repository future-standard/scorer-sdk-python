import cv2
import sys
import os
import scorer

sys.path.append("../lib")
import scorer_util

roi=scorer_util.ROIStorage(os.path.dirname(__file__)+"/switchjudge.json")
x1,y1,x2,y2 = roi.get_roi_rect_by_index(0)
margin=15

cap = scorer.VideoCapture(0)

frame = cap.read()
    
if frame == None:
    sys.exit()

bgr = frame.get_bgr()
bgr = bgr[y1-margin:y2+margin, x1-margin:x2+margin]
cv2.imwrite('image/now.png', bgr)
img_b, img_g, img_r = cv2.split(bgr)
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
img=gray.copy()
#img1 = gray[y1:y2, x1:x2]

#img = cv2.imread('messi5.jpg',0)
template1 = cv2.imread('image/on.png',1)
template2 = cv2.imread('image/off.png',1)
template1_b, template1_g, template1_r = cv2.split(template1)
template2_b, template2_g, template2_r = cv2.split(template2)
template1 = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
template2 = cv2.cvtColor(template2, cv2.COLOR_BGR2GRAY)
w1, h1 = template1.shape[::-1]
w2, h2 = template2.shape[::-1]

# All the 6 methods for comparison in a list
#methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


method = eval('cv2.TM_CCORR_NORMED')

# Apply template Matching
res1 = cv2.matchTemplate(img,template1,method)
res1_b = cv2.matchTemplate(img_b,template1,method)
res1_g = cv2.matchTemplate(img_g,template1,method)
res1_r = cv2.matchTemplate(img_r,template1,method)
res2 = cv2.matchTemplate(img,template2,method)
res2_b = cv2.matchTemplate(img_b,template2,method)
res2_g = cv2.matchTemplate(img_g,template2,method)
res2_r = cv2.matchTemplate(img_r,template2,method)
min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
min_val1_b, max_val1_b, min_loc1_b, max_loc1_b = cv2.minMaxLoc(res1_b)
min_val1_g, max_val1_g, min_loc1_g, max_loc1_g = cv2.minMaxLoc(res1_g)
min_val1_r, max_val1_r, min_loc1_r, max_loc1_r = cv2.minMaxLoc(res1_r)
min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
min_val2_b, max_val2_b, min_loc2_b, max_loc2_b = cv2.minMaxLoc(res2_b)
min_val2_g, max_val2_g, min_loc2_g, max_loc2_g = cv2.minMaxLoc(res2_g)
min_val2_r, max_val2_r, min_loc2_r, max_loc2_r = cv2.minMaxLoc(res2_r)

# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    top_left1 = min_loc1
    top_left2 = min_loc2
else:
    top_left1 = max_loc1
    top_left2 = max_loc2
bottom_right1 = (top_left1[0] + w1, top_left1[1] + h1)
bottom_right2 = (top_left2[0] + w2, top_left2[1] + h2)

img1 = img.copy()
img2 = img.copy()
cv2.rectangle(img1,top_left1, bottom_right1, 255, 2)
cv2.rectangle(img2,top_left2, bottom_right2, 255, 2)
cv2.imwrite("image/res1.jpg",cv2.cvtColor(res1, cv2.COLOR_GRAY2BGR))
cv2.imwrite("image/result1.png",img1)
cv2.imwrite("image/template1.png",template1)
cv2.imwrite("image/res2.jpg",cv2.cvtColor(res2, cv2.COLOR_GRAY2BGR))
cv2.imwrite("image/result2.png",img2)
cv2.imwrite("image/template2.png",template2)
val1=(1-max_val1)*(1-max_val1_b)*(1-max_val1_g)*(1-max_val1_r)
val2=(1-max_val2)*(1-max_val2_b)*(1-max_val2_g)*(1-max_val2_r)

if(val1<val2):
    print("on")
else:
    print("off")
    


print("mixd__on",val1)
print("mixd_off",val2)
"""
print("gray__on",max_val1)
print("gray_off",max_val2)
print("brue__on",max_val1_b)
print("brue_off",max_val2_b)
print("gren__on",max_val1_g)
print("gren_off",max_val2_g)
print("red___on",max_val1_r)
print("red__off",max_val2_r)
"""
