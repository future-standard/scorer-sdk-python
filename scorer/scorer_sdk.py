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

import sys
import zmq
import struct
import cv2
import numpy as np
import time
from datetime import datetime
import pickle

#ZMQ scoket String
sdk_sock_str      = "ipc://@/scorer/logger-sdk"
web_sock1_str     = "ipc://@/scorer/web-sdk1"
web_sock2_str     = "ipc://@/scorer/web-sdk2"
web_sock3_str     = "ipc://@/scorer/web-sdk3"
web_sock4_str     = "ipc://@/scorer/web-sdk4"

# For ZMQ connetion
ctx = zmq.Context()

sdk_sock = ctx.socket(zmq.PUB)
sdk_sock.setsockopt(zmq.SNDHWM, 10000)
sdk_sock.connect(sdk_sock_str)

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
#
upload_interval = 5

def imshow(index, cvmat):
    """Send the opencv image data to Flask web server

    :param cvmat: Opencv image data
    :param index: Web server index
    """
    global web_sock1_bind_set,web_sock2_bind_set,web_sock3_bind_set,web_sock4_bind_set
    serialized = pickle.dumps(cvmat, protocol=4)
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


class Uploader:
    """Uploader class. Class for upload video and log to SCORER cloud server.

    :param task: Task name for log header

    Example::
 
        import scorer

        uploader = scorer.Uploader("TASK")
        uploader.upload(log_str= log_string, images = img_list)

    """
    def __init__(self, task):
        """Initialize the instance

        """
        self.task = task
        self.start=time.time()

    def upload(self, log_dictionary=None, log_list=None, log_str=None, images=None):
        """Upload snapshots image and log to SCORER cloud server

        :param log_dictionary: Dictionary
        :param log_list: List
        :param log_str: String
        :param images: list of numpy images
        :return: upload success then retun True otherwise return False
        """
        end = time.time()

        # Upload interval check
        if end-self.start < upload_interval:
            sys.stderr.write("WRN:Upload interval must have more than " + str(upload_interval) + "sec. This contents are ignored.\n")
            sys.stderr.flush()
            return False

        self.start=time.time()

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
            result_str=str(log_dictionary).replace('{', '(').replace('}', ')')
        if log_list is not None:
            result_str=result_str+str(log_list).replace('[', '(').replace(']', ')')
        if log_str is not None:
            result_str="{" + result_str + "(" + log_str + ")" + "}"

        result_str = result_str.replace(' ', '')
        if len(result_str) == 0:
            result_str="{(Null)}"

        name = "Log".encode('utf-8')
        id = "1".encode('utf-8')

        images_n = len(images) if images is not None else 0

        data = [ name, id, self.task.encode('utf-8'), result_str.encode('utf-8'), np.array( [images_n] ) ]
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
    """
    VideoCapture class. Class for video captureing from camera.
 
    :param index: Camera index
    :param blocking: True if VideoCapture read data as blocking mode
 
    Example::
 
        import scorer
        cap = scorer.VideoCapture(0)

    """
    def __init__(self, index, blocking=True):
        zmq_str = "ipc://@/scorer/frame_grabber-video"
        sock = zmq_str + str(index);
        #
        self.img_sock = ctx.socket(zmq.SUB)
        self.img_sock.setsockopt_string(zmq.SUBSCRIBE, '')
        self.img_sock.setsockopt(zmq.RCVHWM, 1)
        self.img_sock.connect(sock)
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
        """ Get Frame data from VideoCapture

        :return: Frame data
        """
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
        """ Return true if VideoCapture has been ready to read

        :return: True of False
        """
        return not(self.img_sock.closed)

    def release(self):
        """ Close video captureing connection

        """
        self.img_sock.close()

class VideoFrame:
    """VideoFrame class. This class handles frame and date data. VideoCaputre.read() method returns VideoFrame object.

    :param timestamp: timestamp of the frame
    :param format: image format
    :param row: row of the images
    :param col: col of the images
    :param mat_type: mat type of the images
    :param data: image data

    Example::
 
        import scorer
        cap = scorer.VideoCapture(0)
        videoframe = cap.read()

    """
    def __init__(self, timestamp, format, rows, cols, mat_type, data):
        """
        Initialize the instance

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

class LogReceive:
    """LogReceive class. Class for log receiving.

    :param blocking: True if LogReceive read data as blocking mode

    """
    def __init__(self, blocking=True):
        """Initialize the instance

        """
        sock = "ipc://@/scorer/tracker-sdk"
        #
        self.log_sock = ctx.socket(zmq.SUB)
        self.log_sock.setsockopt_string(zmq.SUBSCRIBE, '')
        self.log_sock.setsockopt(zmq.RCVHWM, 1)
        self.log_sock.bind(sock)
        #
        self.poller = zmq.Poller()
        self.poller.register(self.log_sock, zmq.POLLIN)
        #a
        self.blocking=blocking
        if(blocking == True):
            self.timeout = None
        else:
            self.timeout = 0

    def get(self):
        """ Get data from LogReceive

        :return: Log data
        """
        self.events =  dict(self.poller.poll(self.timeout))
        self.count = 0
        try:
            while True:
                socks = self.events
                if self.log_sock in socks and socks[self.log_sock] == zmq.POLLIN:
                    topic, id, log = self.log_sock.recv_multipart(zmq.NOBLOCK, True, False)
                    self.log_data = LogData(log)
                    self.count = 1
        except:
            if self.count == 0:
                return (None)
        return (self.log_data)


    def isOpend(self):
        """ Return true if LogReceive has been ready to read

        :return: True of False
        """
        return not(self.log_sock.closed)

    def release(self):
        """ Close log receiving connection

        """
        self.log_sock.close()

class LogData:
    """LogData class. This class handles log data.

    :param log: Logdata from Scorer

    """
    def __init__(self, log):
        """Initialize the instance

        :param log: log data
        """
        self.log_line = log.decode('utf-8')
        log_array = self.log_line.split()
        self.type = log_array[0]
        self.device = log_array[2]
        self.action = log_array[4]
        self.date = log_array[6]
        self.time = log_array[8]
        self.duration = log_array[10]
        self.diameter = log_array[12]
        self.x = log_array[14]
        self.y = log_array[16]
        self.x_wander = log_array[18]
        self.y_wander = log_array[20]
        self.cross_in = log_array[22]
        self.cross_out = log_array[24]
        self.object_count = log_array[26]
        self.pathway = log_array[28]
        self.snapshot = log_array[30]

    def get_log_line(self):
        return self.log_line

    def get_type(self):
        return self.type

    def get_device(self):
        return self.device

    def get_action(self):
        return self.action

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_duration(self):
        return self.duration

    def get_diameter(self):
        return self.diameter

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_x_wander(self):
        return self.x_wander

    def get_y_wander(self):
        return self.y_wander

    def get_cross_in(self):
        return self.cross_in

    def get_cross_out(self):
        return self.cross_out

    def get_object_count(self):
        return self.object_count

    def get_pathway(self):
        return self.pathway

    def get_snapshot(self):
        return self.snapshot
