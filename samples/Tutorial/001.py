"""
 001.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""
import scorer

# Setup VideoCaputre Object
cap = scorer.VideoCapture(0)

while True:
    # Read Frame from Camera
    frame = cap.read()
    if frame == None:
       continue

    # Convert the Frame to BGR
    bgr = frame.get_bgr()

    # Convert the Frame to Gray
    gray = frame.get_gray()

    # Show the image to Web
    scorer.imshow(1, bgr)
    scorer.imshow(2, gray)
