"""
 recv_sequential.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""

import threading
import struct
import numpy as np

import scorer
import zmq
import cv2

import log_writer

class SequentialReceiver:
    
    def __init__(self, conn_str, recv_timeout):
        self.stop_flag = False
        self.th = threading.Thread(target=self.threadProc, name="th", args = (conn_str,))
        self.timeout = recv_timeout
    
    def start(self):
        self.stop_flag = False
        self.th.start()

    def stop(self):
        self.stop_flag = True
        self.th.join()

    def threadProc(self, conn_str):
        #Open ZMQ Connection
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.setsockopt_string(zmq.SUBSCRIBE, '')
        sock.setsockopt(zmq.RCVHWM, 1)
        sock.connect(conn_str)
        
        poller = zmq.Poller()
        poller.register(sock, zmq.POLLIN)
        
        logger = log_writer.LogWriter()

        while True:
            if (self.stop_flag):
                break

            # Receive Data from C++ Program
            try:
                events =  dict(poller.poll(self.timeout))
                recv_parts = sock.recv_multipart(zmq.NOBLOCK, True, False)
            except:
                continue
            
            # Log
            text = recv_parts[0].decode('utf-8')
            logger.write(text)

            # Image
            if len(recv_parts) > 1:
                # Convert byte to integer
                rows = int.from_bytes(recv_parts[1], 'little')
                cols = int.from_bytes(recv_parts[2], 'little')
        
                # Convert byte to OpenCV Image
                image = np.frombuffer(recv_parts[3], dtype=np.uint8).reshape((rows, cols, 3));

                # Save image
                cv2.imwrite("hvcp2.bmp", image);
#                scorer.imshow(1, image)

