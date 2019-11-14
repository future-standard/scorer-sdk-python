import scorer
import cv2
import numpy as np
import logging
from tracked_object import *
#from pykalman import KalmanFilter

TRACK_DISTANCE_THRESHOLD = 4.0
TRACK_HIST_LENGTH = 1024


class object_tracker:
    def __init__(self, save_logs_, save_snapshots_, imshow_, sharpening4_, sharpening8_, endurance_sec_, maturity_sec_, after_moment_sec_, wanderer_epsilon_):
        self._object_id = 1
        self._rois = np.array([])
        self._objs_to_track = np.array([])
        self._objs = np.array([])
        self._lost = np.array([])
        self._save_logs = save_logs_
        self._save_snapshots = save_snapshots_
        self._sharpening4 = sharpening4_
        self._sharpening8 = sharpening8_
        self._imshow = imshow_
        self._endurance_sec = endurance_sec_
        self._maturity_sec = maturity_sec_
        self._after_moment_sec = after_moment_sec_
        self._wanderer_epsilon = wanderer_epsilon_

        if self._save_logs:
            # Process Log
            self._pro_logger = logging.getLogger('pro_log')
            self._pro_logger.setLevel(10)
            pro_log = logging.FileHandler('log/progress.log')
            self._pro_logger.addHandler(pro_log)
            pro_stream = logging.StreamHandler()
            self._pro_logger.addHandler(pro_stream)

            #Lost face log
            self._lost_logger = logging.getLogger('lost_log')
            self._lost_logger.setLevel(10)
            lost_log = logging.FileHandler('log/lost_faces.log')
            self._lost_logger.addHandler(lost_log)
            lost_stream = logging.StreamHandler()
            self._lost_logger.addHandler(lost_stream)


    def track_objects(self, rois_, image_, timestamp_):
        # Initialize
        self._rois = rois_
        self._objs_to_track = np.copy(self._objs)
        self._objs = np.array([])
        self._lost = np.array([])
        nrois = len(self._rois)
        nobjs = len(self._objs_to_track)
        matches = []

        # Match rois and obj
        if nobjs > 0:
            for i in range(nrois):
                min_dist = center_distance(self._objs_to_track[0], rois_[i])
                closest = 0

                for j in range(nobjs):
                    dist = center_distance(self._objs_to_track[j], rois_[i])
                    if dist < min_dist:
                        min_dist = dist
                        closest = j
            
                if is_neighbor_distance(self._objs_to_track[closest], min_dist):
                    matches.append(rod(i, closest, min_dist))

        nmatches = len(matches)

        # Cut extra obj
        if nmatches > 0:
            for i in range(nobjs):
                min_dist = 0.0
                closest_roi = -1
                match_idx = -1

                for j in range(nmatches):
                    if i != matches[j].obj_index:
                        continue

                    if match_idx == -1:
                        min_dist = matches[j].distance
                        closest_roi = matches[j].roi_index
                        match_idx = j

                    elif min_dist > matches[j].distance:
                        matches[j].obj_index = -1
                        min_dist = matches[j].distance
                        closest_roi = matches[j].roi_index
                        match_idx = j
                    else:
                        matches[j].obj_index = -1

        # Create push array
        roi_pushed = [0] * nrois
        obj_pushed = [0] * nobjs

        # Update information
        for m in matches:
            if m.obj_index == -1:
                continue

            roi = rois_[m.roi_index]
            obj = self._objs_to_track[m.obj_index]

            self._objs = np.append(self._objs, obj)
            self._objs[-1].follow(roi, image_, timestamp_)
        
            roi_pushed[m.roi_index] += 1
            obj_pushed[m.obj_index] += 1

        # Create new instance
        for i in range(nrois):
            if roi_pushed[i] == 0:
                self._objs = np.append(self._objs, tracked_object(self._object_id, rois_[i], image_, timestamp_, self._save_snapshots,
                    self._sharpening4, self._sharpening8, self._endurance_sec, self._maturity_sec, self._after_moment_sec, self._wanderer_epsilon))
                self._object_id += 1

        # Detect lost
        for i in range(nobjs):
            if obj_pushed[i] == 0:
                obj = self._objs_to_track[i]
                obj.occluded()

                if obj.is_lost(timestamp_):
                    self._lost = np.append(self._lost, obj)
                else:
                    self._objs = np.append(self._objs, obj)

        if self._save_logs:
            if self._rois.shape[0] > 0 or self._objs_to_track.shape[0] > 0 or self._objs.shape[0] > 0 or self._lost.shape[0] > 0:
                self._pro_logger.log(20, timestamp_)
                self._pro_logger.log(20, 'Inputed objects:' + str(self._rois.shape[0]))
                self._pro_logger.log(20, 'Tracked objects last time:' + str(self._objs_to_track.shape[0]))
                self._pro_logger.log(20, 'Tracked objects this time:' + str(self._objs.shape[0]))
                self._pro_logger.log(20, 'Losted objects:' + str(self._lost.shape[0]) + '\n')

            for i in range(self._lost.shape[0]):
                log = 'Object ID:' + str(self._lost[i]._object_id)
                self._lost_logger.log(20, log)
                log = 'Tracking Start:' + str(self._lost[i]._start)
                self._lost_logger.log(20, log)
                for j in range(self._lost[i]._time_hist.shape[0]):
                    log = str(self._lost[i]._time_hist[j]) + str(self._lost[i]._center_hist[j])
                    self._lost_logger.log(20, log)
                log = 'Tracking End:' + str(self._lost[i]._last_seen) + '\n'
                self._lost_logger.log(20, log)
        
        # Imshow        
        if self._imshow:
            for i in range(self._objs.shape[0]):
                if (self._objs[i]._last_seen -  self._objs[i]._start).total_seconds() > self._after_moment_sec:
                    image_ = cv2.rectangle(image_, (int(self._objs[i]._roi[0]), int(self._objs[i]._roi[1])),
                        (int(self._objs[i]._roi[0] + self._objs[i]._roi[2]), int(self._objs[i]._roi[1] + self._objs[i]._roi[3])), (0, 0, 255), 3)
                else:
                    image_ = cv2.rectangle(image_, (int(self._objs[i]._roi[0]), int(self._objs[i]._roi[1])),
                        (int(self._objs[i]._roi[0] + self._objs[i]._roi[2]), int(self._objs[i]._roi[1] + self._objs[i]._roi[3])), (0, 255, 0), 3)
                
                for j in range(self._objs[i]._center_hist.shape[0]):
                    image_ = cv2.circle(image_, (int(self._objs[i]._center_hist[j][0]), 
                                int(self._objs[i]._center_hist[j][1])), 5, (0, 0, 0), -1)
                    if j > 0:
                        image_ = cv2.line(image_, (int(self._objs[i]._center_hist[j - 1][0]), 
                                        int(self._objs[i]._center_hist[j - 1][1])),
                                    (int(self._objs[i]._center_hist[j][0]), 
                                        int(self._objs[i]._center_hist[j][1])), (0, 0, 0), 2)
                
            scorer.imshow(1, image_)

    def result(self):
        return self._lost
