# -*- coding: utf-8 -*-
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

import numpy as np
import re
import json
import os

home=os.getenv('HOME')

ROI_FILE=home + "/scorer-sdk-python/samples/lib/user_roi.json"

class ROIStorage:
    """ROI data strage class. Class for data starge of ROI data
    """
    def __init__(self, roi_file='default'):
        self.roi_file = roi_file

        if self.roi_file == "default":
            roi_fname = ROI_FILE
        else:
            roi_fname=self.roi_file
    
        try:
            user_roi_file = open(roi_fname, 'r')
        except IOError:
            print("ERROR:Can not Open ROI Configuration file. [" + ROI_FILE  + "]")
            exit(1)
    
        data = json.load(user_roi_file)
        user_roi_file.close()
    
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
