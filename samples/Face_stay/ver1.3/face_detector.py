import cv2
import numpy as np
import logging
import os

# Background Subtractor MOG2 parameters
MOG2_HISTORY_LENGTH = 50
MOG2_MAHALANOBIS_THRESHOLD = 16
MOG2_DETECT_SHADOWS = False
MOG2_LEARNING_RATE = -1
MOG2_DETECT_IMAGE_WIDTH = 40

# The Cascade classifier params
CASCADE_PATH = 'cascade/haarcascade_frontalface_alt2.xml'
CASCADE_SCALE_FACTOR = 1.11
CASCADE_MIN_NEIGHBORS = 3
CASCADE_FLAGS = 0
CASCADE_MIN_OBJECT_SIZE = (30, 30)
CASCADE_MAX_OBJECT_SIZE = (500, 500)
CASCADE_MIN_MOG2_DENSITY = 0.10

LOG_PATH = 'log/'


class face_detector:
    def __init__(self, save_logs_):
        self._detected = np.array([])
        self.bgr = None
        self.time = None
        self._thumbnail = np.zeros(3)
        self._bgsub = None
        self._fgmask = np.zeros(3)
        self._save_logs = save_logs_

        try:
            self._cascade = cv2.CascadeClassifier(CASCADE_PATH)
        except:
            print('Face cascade is not found')
        
        if not os.path.isdir(LOG_PATH):
            os.makedirs(LOG_PATH)

        if self._save_logs:
            self._logger = logging.getLogger('detect_log')
            self._logger.setLevel(10)
            log = logging.FileHandler(LOG_PATH + 'detect.log')
            self._logger.addHandler(log)
            stream = logging.StreamHandler()
            self._logger.addHandler(stream)


    def detect(self, img, time):
        # Get bgr and gray and time
        self.bgr = img
        gray = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2GRAY)
        self.time = time

        # Get img height and width
        imgheight, imgwidth, _ = self.bgr.shape

        # Create thumbnail
        scale = 1.0 * MOG2_DETECT_IMAGE_WIDTH / imgwidth
        height = int(imgheight * scale)
        size = tuple([MOG2_DETECT_IMAGE_WIDTH, height])
        self._thumbnail = cv2.resize(self.bgr, size, cv2.INTER_AREA)

        # Get bgsub
        if (self._fgmask.size * 3) != self._thumbnail.size or self._bgsub == None:
            self._bgsub = cv2.createBackgroundSubtractorMOG2(MOG2_HISTORY_LENGTH, 
                    MOG2_MAHALANOBIS_THRESHOLD, MOG2_DETECT_SHADOWS)

        # Apply mask
        self._fgmask = self._bgsub.apply(self._thumbnail, MOG2_LEARNING_RATE)
        ret, fgmask_binary = cv2.threshold(self._fgmask, 200, 255, cv2.THRESH_BINARY)
        fgsum = cv2.integral(fgmask_binary)

        # Create unified array
        unified = np.array([])

        #Detect face
        self._detected = self._cascade.detectMultiScale(gray, CASCADE_SCALE_FACTOR, CASCADE_MIN_NEIGHBORS, 
                    CASCADE_FLAGS, CASCADE_MIN_OBJECT_SIZE, CASCADE_MAX_OBJECT_SIZE)

        n = len(self._detected)

        for i in range(n):
            r = self._detected[i]
            contained = False

            # Check duplication
            for j in range(i + 1, n):
                s = self._detected[j]
                if r[0] <= s[0] and r[1] <= s[1] and (s[0] + s[2]) <= (r[0] + r[2]) and (s[1] + s[3]) <= (r[1] + r[3]):
                    self._detected[j] = r
                    contained = True
                    break;
                if s[0] <= r[0] and s[1] <= r[1] and (r[0] + r[2]) <= (s[0] + s[2]) and (r[1] + r[3]) <= (s[1] + s[3]):
                    contained = True
                    break

            # Check density
            if not contained:
                x1 = int(r[0] * scale)
                y1 = int(r[1] * scale)
                x2 = int((r[0] + r[2]) * scale)
                y2 = int((r[1] + r[3]) * scale)

                area_total = 0          
                for i in range(y1, y2):
                    for j in range(x1, x2):
                        if fgsum.item(i, j) > 0:
                            area_total += 1
                density = 1.0 * area_total / ((x2 - x1) * (y2 - y1))
            
                if density > CASCADE_MIN_MOG2_DENSITY:
                    r = r.reshape(1, 4)
                    if unified.size == 0:
                        unified = r.copy()
                    else:
                        unified = np.append(unified, r, axis=0)

        # Copy result
        self._detected = unified.copy()

        # Log
        if self._save_logs and len(self._detected) > 0:
            self._logger.log(20, time)
            for i in range(len(self._detected)):
                log = 'No' + str(i + 1) + ':' + str(self._detected[i])
                self._logger.log(20, log)
            log = 'Detected Num:' + str(len(self._detected)) + '\n'
            self._logger.log(20, log)


    def result(self):
        return self._detected, self.bgr, self.time
