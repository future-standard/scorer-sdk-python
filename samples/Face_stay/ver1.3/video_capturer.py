import scorer
import cv2
from datetime import datetime


class video_capturer:
    def __init__(self, mode, url = None):
        self._mode = mode

        if self._mode == "scorer":
            self._cap = scorer.VideoCapture(0)
        
        if self._mode == "rtsp":
            self._capture = cv2.VideoCapture(url)


    def get_image(self):
        img = None
        time = None
        if self._mode == "scorer":
            # Capture
            frame = None
            while frame == None:
                frame = self._cap.read()
            img = frame.get_bgr() 
            time = frame.datetime
        elif self._mode == "rtsp":
            # Capture
            ret = None
            while ret == None:
                ret, img = self._capture.read()
                time = datetime.now()
                cv2.waitKey(1)
        return img, time
