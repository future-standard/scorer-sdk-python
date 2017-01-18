# -*- coding: utf-8 -*-
"""Scorer.py  Main library code of Scorer SDK for python
This is a main socuce code of Scorer SDK for python.<br>
It collaborate with Scorer for Raspberry Pi.
"""
#Copyright 2017 Future Standard Co., Ltd.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import zmq
import struct
import cv2
import numpy as np
import time
import re
import json
from datetime import datetime
import pickle

#ZMQ scoket String
img_sock_str      = "ipc://@/scorer/frame_grabber-video0"
sdk_sock_str      = "ipc://@/scorer/logger-sdk"
web_sock1_str     = "ipc://@/scorer/web-sdk1"
web_sock2_str     = "ipc://@/scorer/web-sdk2"
web_sock3_str     = "ipc://@/scorer/web-sdk3"
web_sock4_str     = "ipc://@/scorer/web-sdk4"
MAX_WEB_SCOCK  = 4

SCORER_DEV_CONFIG = "/opt/scorer/home/dev/lib/CONFIG"
USER_ROI_DATA = "USER_ROI_DATA="

# For ZMQ connetion
ctx = zmq.Context()

sdk_sock = ctx.socket(zmq.PUB)
sdk_sock.setsockopt(zmq.SNDHWM, 10000)
sdk_sock.connect(sdk_sock_str)

task = "SDK"

# For web_show
web_sock1 = ctx.socket(zmq.PUB)
web_sock1.setsockopt(zmq.SNDHWM, 10000)
#
web_sock2 = ctx.socket(zmq.PUB)
web_sock2.setsockopt(zmq.SNDHWM, 10000)
#
web_sock3 = ctx.socket(zmq.PUB)
web_sock3.setsockopt(zmq.SNDHWM, 10000)
#
web_sock4 = ctx.socket(zmq.PUB)
web_sock4.setsockopt(zmq.SNDHWM, 10000)
#
web_sock1_bind_set = False
web_sock2_bind_set = False
web_sock3_bind_set = False
web_sock4_bind_set = False


def imshow(index, cvmat):
    """Send the opencv image data to Flask web server

    :param cvdata: Opencv image data
    :param index: Web server index
    """
    serialized = pickle.dumps(cvdata, protocol=4)
    if index == 1:
        if web_sock1_bind_set == False:
            web_sock1_bind_set = True
            web_sock1.bind(web_sock1_str)

        web_sock1.send(serialized)
    elif index == 2:
        if web_sock2_bind_set == False:
            web_sock2_bind_set = True
            web_sock2.bind(web_sock2_str)

        web_sock2.send(serialized)
    elif index == 3:
        if web_sock3_bind_set == False:
            web_sock3_bind_set = True
            web_sock3.bind(web_sock3_str)

        web_sock3.send(serialized)
    elif index == 4:
        if web_sock4_bind_set == False:
            web_sock4_bind_set = True
            web_sock4.bind(web_sock4_str)

        web_sock4.send(serialized)
    else:
        print("the index[" + index + "] is invalid")
        return False
    return True

def upload(log_dictionary=None, log_list=None, log_str=None, images=None):
    """upload Upload snapshots image and log

    :param log_dictionary: Dictionary
    :param log_list: List
    :param log_str: String
    :param images: list of numpy images
    :return: upload success then retun True otherwise return False
    """
    result_str=""

    # Syntax check
    if log_dictionary is not None and isinstance(log_dictionary, dict) == False:
         print("log_dictionary is not a dictionary")
         return False

    if log_list is not None and isinstance(log_list, list) == False:
         print("log_list is not a list")
         return False

    if log_str is not None and isinstance(log_str, str) == False:
         print("log_str is not a String")
         return False

    if images is not None and isinstance(images, list) == False:
         print("images is not a list")
         return False

    if images is not None and len(images) >= 6:
        print("images list len must be less than 5")
        return False;

    # Combine the log payload text
    if log_dictionary is not None:
        result_str=str(log_dictionary)
    if log_list is not None:
        result_str=result_str+str(log_list)
    if log_str is not None:
        result_str=result_str + "(" + log_str + ")"

    result_str = result_str.replace(' ', '')
    if len(result_str) == 0:
        result_str="\"\""

    name = "Log".encode('utf-8')
    id = "1".encode('utf-8')

    images_n = len(images) if images is not None else 0

    data = [ name, id, task.encode('utf-8'), result_str.encode('utf-8'), np.array( [images_n] ) ]
    sdk_sock.send_multipart(data, zmq.SNDMORE )

    # If no images, just send log payload
    if images_n == 0:
            sdk_sock.send_multipart(data)
            return True

    # Send images and log payload
    for i in range( images_n ):
        height, width = images[i].shape[:2]
        ndim = images[i].ndim
        data_info = np.array( [height, width, ndim] );

        data = [ data_info, images[i].data ]
        if i == len(images) -1:
            sdk_sock.send_multipart(data)
        else:
            sdk_sock.send_multipart(data, zmq.SNDMORE)

    return True

class VideoCapture:
    """VideoCapture class. Class for video captureing from camera.
    """
    def __init__(self, index, blocking=True):
        zmq_str = "ipc://@/scorer/frame_grabber-video"
        sock = zmq_str + str(index);
        #
        self.img_sock = ctx.socket(zmq.SUB)
        self.img_sock.setsockopt_string(zmq.SUBSCRIBE, '')
        self.img_sock.setsockopt(zmq.RCVHWM, 1)
        self.img_sock.connect(img_sock)
        #
        self.poller = zmq.Poller()
        self.poller.register(self.img_sock, zmq.POLLIN)
        #a
        self.blocking=blocking
        if(blocking == True):
            self.timeout = None
        else:
            self.timeout = 0

    def read(self):
        self.events =  dict(self.poller.poll(self.timeout))
        self.count = 0
        try:
            while True:
                socks = self.events
                if self.img_sock in socks and socks[self.img_sock] == zmq.POLLIN:
                    topic, id, timestamp, my_type, format, rows, cols, mat_type, data = \
                                             self.img_sock.recv_multipart(zmq.NOBLOCK, True, False)
                    self.frame = VideoFrame(timestamp, format, rows, cols, mat_type, data)
                    self.count = 1
        except:
            if self.count == 0:
                return (None)
        return (self.frame)


    def isOpend(self):
        return self.img_sock.closed

    def release(self):
        self.img_sock.close()

class VideoFrame:
    """VideoFrame class. This class handles frame and date data.
    """
    def __init__(self, timestamp, format, rows, cols, mat_type, data):
        """Initialize the instance

        :param timestamp: timestamp of the frame
        :param format: image format
        :param row: row of the images
        :param col: col of the images
        :param mat_type: mat type of the images
        :param data: image data
        """
        self.my_time = struct.unpack('!q', timestamp)
        self.my_row = struct.unpack('!i', rows)
        self.my_col = struct.unpack('!i', cols)
        self.my_type = struct.unpack('!i', mat_type)
        self.image = np.frombuffer(data, dtype=np.uint8).reshape((self.my_row[0],self.my_col[0]));
        self.image_format=format.decode('utf-8')

        epoch_time = self.my_time[0]/1000000
        epoch_msec = self.my_time[0]%1000000

        self.width = self.my_col[0]
        self.height = self.my_row[0]
        self.time = self.my_time[0]
        self.datetime= datetime(*time.localtime(epoch_time)[:6])
        self.msec= epoch_msec

    def get_bgr(self):
        """ Get bgr image data

        :return: bgr image data
        """
        if self.image_format == "I420":
            bgr = cv2.cvtColor(self.image, cv2.COLOR_YUV2BGR_I420)
        elif self.image_format == "BGR":
            bgr = self.image
        elif self.image_format == "RGBA":
            bgr = cv2.cvtColor(self.image, cv2.COLOR_RGBA2BGR)
        else:
            raise Exception("format is incorrect")
        return bgr

    def get_gray(self):
        """Get gray image data

        :return: gray image data
        """
        if self.image_format == "I420":
            gray = cv2.cvtColor(self.image, cv2.COLOR_YUV2GRAY_I420)
        elif self.image_format == "BGR":
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        elif self.image_format == "RGBA":
            gray = cv2.cvtColor(self.image, cv2.COLOR_RGBA2BGR)
        else:
            raise Exception("format is incorrect")
        return gray

    def get_frame_time(self):
        """Get frame timestamp

        :return: timestamp of this image
        """
        return self.my_time[0]
 
    def get_frame_datetime(self):
        """Get frame datetime

        :return: datetime
        """
        epoch_time = self.my_time[0]/1000000;
        return datetime(*time.localtime(epoch_time)[:6])
 
    def get_frame_msec(self):
        """Get frame msec

        :return: msec
        """
        epoch_msec = self.my_time[0]%1000000;
        return epoch_msec
     
class Scorer:
    """ Scorer SDK main class.  This is the main class of Scorer SDK
    """
    def __init__(self, task, roi_file='default'):
        """Initialize the instance

        :param task: Task name
        """
        ctx = zmq.Context()
        #
        if task is None or isinstance(task, str) == False:
            raise Exception("task type is incorrect")
        if len(task) == 0:
            raise Exception("task has length 0")
        self.task = task
        #
        self.img_sock = ctx.socket(zmq.SUB)
        self.img_sock.setsockopt_string(zmq.SUBSCRIBE, '')
        self.img_sock.setsockopt(zmq.RCVHWM, 1)
        self.img_sock.connect(img_sock)
        #
        self.sdk_sock = ctx.socket(zmq.PUB)
        self.sdk_sock.setsockopt(zmq.SNDHWM, 10000)
        self.sdk_sock.connect(sdk_sock)
        #
        self.poller = zmq.Poller()
        self.poller.register(self.img_sock, zmq.POLLIN)
        #
        self.web_sock1 = ctx.socket(zmq.PUB)
        self.web_sock1.setsockopt(zmq.SNDHWM, 10000)
        #
        self.web_sock2 = ctx.socket(zmq.PUB)
        self.web_sock2.setsockopt(zmq.SNDHWM, 10000)
        #
        self.web_sock3 = ctx.socket(zmq.PUB)
        self.web_sock3.setsockopt(zmq.SNDHWM, 10000)
        #
        self.web_sock4 = ctx.socket(zmq.PUB)
        self.web_sock4.setsockopt(zmq.SNDHWM, 10000)
        #
        self.web_sock1_bind_set = False
        self.web_sock2_bind_set = False
        self.web_sock3_bind_set = False
        self.web_sock4_bind_set = False

        try:
            config_file = open(SCORER_DEV_CONFIG, 'r')
        except IOError:
            print("ERROR:Can not Open Scorer Configuration file.")
            exit(1)

        for line in config_file.readlines():
            line = re.sub(r'#.*$', "", line)
            matchOB = re.match(USER_ROI_DATA , line)
            if matchOB == None:
                continue
            name, roi_fname = line[:-1].split('=')
            break

        if roi_file!="default":
            roi_fname=roi_file

        try:
            user_roi_file = open(roi_fname, 'r')
        except IOError:
            print("ERROR:Can not Open ROI Configuration file.")
            exit(1)

        data = json.load(user_roi_file)

        keyList = data.keys()

        for k in keyList:
            if k != "objects":
                continue
            roiObjects = data[k]
            break

        roiObjects_n = len(roiObjects)
        self.circle_list = []
        self.line_list = []
        self.rect_list = []
        self.all_list = []
        for roi in roiObjects:
            try:
                my_type = roi["type"]
            except KeyError:
                continue

            if my_type == "circle":
                id = roi["id"]
                x = roi["points"]["x"]
                y = roi["points"]["y"]
                radius =  roi["radius"]
                self.circle_list.append({"id": id, "x": x, "y": y, "radius": radius })
            elif  my_type == "line":
                id = roi["id"]
                x1 = roi["points"][0]["x"]
                y1 = roi["points"][0]["y"]
                x2 = roi["points"][1]["x"]
                y2 = roi["points"][1]["y"]
                self.line_list.append({"id": id, "x1": x1, "y1": y1, "x2": x2, "y2": y2 })
            elif  my_type == "rect":
                id = roi["id"]
                x1 = roi["points"][0]["x"]
                y1 = roi["points"][0]["y"]
                x2 = roi["points"][1]["x"]
                y2 = roi["points"][1]["y"]
                self.rect_list.append({"id": id, "x1": x1, "y1": y1, "x2": x2, "y2": y2 })
            elif  my_type == "path":
                print("")
            else:
                continue

        config_file.close()
        user_roi_file.close()


    def get_roi_circle(self):
        """Get ROI Circle data

        :return: List of ROI data for Circle
        """
        return self.circle_list

    def get_roi_circle_len(self):
        """Get ROI Circle data

        :return: Length of ROI data for Circle
        """
        return len(self.circle_list)

    def get_roi_circle_by_index(self, index):
        """Get ROI Circle data by index

        :param index: index
        :return: ROI data of Circle by index (x y radius)
        """
        return int(self.circle_list[index]["x"]), int(self.circle_list[index]["y"]), int(self.circle_list[index]["radius"])

    def get_roi_rect(self):
        """Get ROI Rectangle data

        :return: List of ROI data for Rectangle
        """
        return self.rect_list

    def get_roi_rect_len(self):
        """Get ROI Rectangle data length

        :return: Length of ROI data for Rectangle
        """
        return len(self.rect_list)

    def get_roi_rect_by_index(self, index):
        """Get ROI Rectangle data by index

        :param int index: index
        :return: ROI data of Rectangle by index (x1 y1 x2 y2)
        """
        return int(self.rect_list[index]["x1"]), int(self.rect_list[index]["y1"]), \
               int(self.rect_list[index]["x2"]), int(self.rect_list[index]["y2"])

    def get_roi_line(self):
        """Get ROI Line data

        :return: List of ROI data for Line
        """
        return self.line_list

    def get_roi_line_len(self):
        """Get ROI Line data length

        :return: Length of ROI data for Line
        """
        return len(self.line_list)

    def get_roi_line_by_index(self, index):
        """Get ROI Line data by index

        :param index: index
        :return: ROI data of Line by index (x1 y1 x2 y2)
        """
        return int(self.line_list[index]["x1"]), int(self.line_list[index]["y1"]), \
               int(self.line_list[index]["x2"]), int(self.line_list[index]["y2"])

    def poll(self, timeout=None):
        """Poller for zmq

        :param timeout: timeout(s)
        """
        self.events =  dict(self.poller.poll(timeout))
        if len(self.events) == 0:
            return False
        else:
            return True

    def get_frame(self):
        """Get frame data from zmq

        :param block_type: block_type
        """
        self.count = 0
        try:
            while True:
                socks = self.events
                if self.img_sock in socks and socks[self.img_sock] == zmq.POLLIN:
                    topic, id, timestamp, my_type, format, rows, cols, mat_type, data = \
                                             self.img_sock.recv_multipart(zmq.NOBLOCK, True, False)
                    self.frame = VideoFrame(timestamp, format, rows, cols, mat_type, data)
                    self.count = 1
        except:
            if self.count == 0:
                return (None)
        return (self.frame)            

    def web_show(self, cvdata, index):
        """Send the opencv image data to Flask web server

        :param cvdata: Opencv image data
        :param index: Web server index
        """
        serialized = pickle.dumps(cvdata, protocol=4)
        if index == 1:
            if self.web_sock1_bind_set == False:
                self.web_sock1_bind_set = True
                self.web_sock1.bind(web_sock1)

            self.web_sock1.send(serialized)
        elif index == 2:
            if self.web_sock2_bind_set == False:
                self.web_sock2_bind_set = True
                self.web_sock2.bind(web_sock2)

            self.web_sock2.send(serialized)
        elif index == 3:
            if self.web_sock3_bind_set == False:
                self.web_sock3_bind_set = True
                self.web_sock3.bind(web_sock3)

            self.web_sock3.send(serialized)
        elif index == 4:
            if self.web_sock4_bind_set == False:
                self.web_sock4_bind_set = True
                self.web_sock4.bind(web_sock4)

            self.web_sock4.send(serialized)
        else:
            print("the index[" + index + "] is invalid")
            return False
        return True

    def upload(self, log_dictionary=None, log_list=None, log_str=None, images=None):
        """upload Upload snapshots image and log

        :param log_dictionary: Dictionary
        :param log_list: List
        :param log_str: String
        :param images: list of numpy images
        :return: upload success then retun True otherwise return False
        """
        result_str=""

        # Syntax check
        if log_dictionary is not None and isinstance(log_dictionary, dict) == False:
             print("log_dictionary is not a dictionary")
             return False
     
        if log_list is not None and isinstance(log_list, list) == False:
             print("log_list is not a list")
             return False
     
        if log_str is not None and isinstance(log_str, str) == False:
             print("log_str is not a String")
             return False

        if images is not None and isinstance(images, list) == False:
             print("images is not a list")
             return False

        if images is not None and len(images) >= 6:
            print("images list len must be less than 5")
            return False;
     
        # Combine the log payload text
        if log_dictionary is not None:
            result_str=str(log_dictionary)
        if log_list is not None:
            result_str=result_str+str(log_list)
        if log_str is not None:
            result_str=result_str + "(" + log_str + ")"

        result_str = result_str.replace(' ', '')
        if len(result_str) == 0:
            result_str="\"\""

        name = "Log".encode('utf-8')
        id = "1".encode('utf-8')

        images_n = len(images) if images is not None else 0

        data = [ name, id, self.task.encode('utf-8'), result_str.encode('utf-8'), np.array( [images_n] ) ]
        self.sdk_sock.send_multipart(data, zmq.SNDMORE )

        # If no images, just send log payload
        if images_n == 0:
                self.sdk_sock.send_multipart(data)
                return True

        # Send images and log payload
        for i in range( images_n ):
            height, width = images[i].shape[:2]
            ndim = images[i].ndim
            data_info = np.array( [height, width, ndim] );

            data = [ data_info, images[i].data ]
            if i == len(images) -1:
                self.sdk_sock.send_multipart(data)
            else:
                self.sdk_sock.send_multipart(data, zmq.SNDMORE)

        return True
