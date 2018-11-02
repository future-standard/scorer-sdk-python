import scorer
import cv2
import numpy as np
from enum import Enum
from pykalman import UnscentedKalmanFilter

# Object tracker params
TRACK_ENDURANCE_THRESHOLD = 3
TRACK_MATURITY_THRESHOLD = 1
TRACK_AFTER_A_MOMENT_TIME = 3
TRACK_WANDERER_EPSILON = 0.01

TRACK_DISTANCE_THRESHOLD = 4.0
TRACK_HIST_LENGTH = 1024


class cross_direction(Enum):
	L2R = 0
	R2L = 1
	T2B = 2
	B2T = 3


class tracking_state(Enum):
	SEEN = 0
	OCCLUDED = 1
	LOST = 2


class rod:
        def __init__(self, roi_index_, obj_index_, distance_):
                self.roi_index = roi_index_
                self.obj_index = obj_index_
                self.distance = distance_


class tracked_object:
	def __init__(self, object_id_, roi_, image_, t_, keep_snapshots_, sharpening4_, sharpening8_,
			endurance_sec_ = TRACK_ENDURANCE_THRESHOLD, maturity_sec_ = TRACK_MATURITY_THRESHOLD, 
			after_moment_sec_ = TRACK_AFTER_A_MOMENT_TIME, wanderer_epsilon_ = TRACK_WANDERER_EPSILON):
		self._object_id = object_id_
		self._center = np.array([roi_[0] + roi_[2] / 2, roi_[1] + roi_[3] / 2])
		self._radius = (roi_[2] + roi_[3]) / 4
		self._roi = roi_.copy()
		self._center_ema = self._center
		self._radius_ema = self._radius
		self._center0 = self._center
		self._radius0 = self._radius
		self._center1 = np.array([0, 0])
		self._radius1 = 0
		self._roi0 = self._roi.copy()
		self._roi1 = np.array([])
		self._roi2 = self._roi.copy()
		self._wander = np.array([self._center, [0, 0]])
		_, self._width, _ = image_.shape
		self._height, _, _ = image_.shape
		self._snapshot1 = np.array([])
		self._center_hist = np.array([self._center]).reshape(1, 2)
		self._radius_hist = np.array([self._radius])
		self._time_hist = np.array([t_])
		self._start = t_
		self._stop = t_
		self._last_seen = t_
		self._state = tracking_state.SEEN
		self._cross_in = np.array([0, 0, 0, 0])
		self._cross_out = np.array([0, 0, 0, 0])
		self._keep_snapshots = keep_snapshots_
		self._threshold_endurance_sec = endurance_sec_
		self._threshold_maturity_sec = maturity_sec_
		self._threshold_after_moment_sec = after_moment_sec_
		self._threshold_wanderer_epsilon = wanderer_epsilon_
		self.stream_tag = ''
		self.object_color = ''
		self.extra_rois = '' 
		self.snapshot_names = ''
		self._sharpening4 = sharpening4_
		self._sharpening8 = sharpening8_

		#Kalman
		#self._ukf = UnscentedKalmanFilter(f, g, observation_covariance=0.1)
		#self._prediction = np.array(self._ukf.filter(self._center)[0]).reshape(1, 2)

		if self._keep_snapshots:
			self._snapshot0 = image_.copy()
			self._snapshot2 = image_.copy()
			self._snapshot = image_.copy()
		else:
			self._snapshot0 = np.array([])
			self._snapshot2 = np.array([])
			self._snapshot = np.array([])

		if self._sharpening4:
			self._kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
		if self._sharpening8:
			self._kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], np.float32)


	def follow(self, roi_, image_, t_):
		if self._keep_snapshots:
			self._snapshot = image_.copy()

		h, w, c = image_.shape
		if self._width != w or self._height != h:
			print('The resolution has changed; do not track this object anymore.')
			return

		self._center = np.array([roi_[0] + roi_[2] / 2, roi_[1] + roi_[3] / 2])
		self._radius = (roi_[2] + roi_[3]) / 4
		self._roi = roi_.copy()

		#Kalman
		#self._prediction = np.append(self._prediction, self._ukf.filter(self._center)[0].reshape(1, 2), axis=0)

		self._center_ema = self._center * 0.0625 + self._center_ema * 0.9375
		self._radius_ema = self._radius * 0.0625 + self._radius_ema * 0.9375

		self.wander = np.array([self._center, self._wander[0]])

		if abs(self.wander[0][0] - self.wander[1][0]) > self._threshold_wanderer_epsilon * w or abs(self.wander[0][1] - self.wander[1][1]) > self._threshold_wanderer_epsilon * h:
			if self._center_hist.shape[0] < TRACK_HIST_LENGTH:
				copy = self._center.copy().reshape(1, 2)
				self._center_hist = np.append(self._center_hist, copy, axis=0)
				self._radius_hist = np.append(self._radius_hist, self._radius)
				self._time_hist = np.append(self._time_hist, t_)
			else:
				self._center_hist[TRACK_HIST_LENGTH - 1] = self._center;
				self._radius_hist[TRACK_HIST_LENGTH - 1] = self._radius;

			if self._keep_snapshots and self._snapshot1.shape[0] == 0 and (t_ - self._start).total_seconds() > self._threshold_after_moment_sec:
				self._snapshot1 = image_.copy()
				self._center1 = self._center
				self._center2 = self._center
				self._roi1 = self._roi

		
		if abs(self.wander[0][0] - self.wander[1][0]) < 0.5 * w or abs(self.wander[0][1] - self.wander[1][1]) < 0.5 * h:
			if rect_area(self._roi2) < rect_area(roi_):
				self._roi2 = roi_

				if self._keep_snapshots:
					self._snapshot2 = image_.copy()
		
		self._last_seen = t_
		self._status = tracking_state.SEEN

	def occluded(self):
		self._state = tracking_state.OCCLUDED


	def is_lost(self, t_):
		if self._state == tracking_state.OCCLUDED and (t_ - self._last_seen).total_seconds() < self._threshold_endurance_sec:
			return False

		if self._sharpening4 or self._sharpening8:
			self._snapshot2 = cv2.filter2D(self._snapshot2, -1, self._kernel)

		self._stop = self._last_seen
		self._state = tracking_state.LOST
		return True


def center_distance(obj_, roi_):
	roi_center = np.array([roi_[0] + roi_[2] / 2, roi_[1] + roi_[3] / 2])
	d = roi_center - obj_._center;
	return np.sqrt(d[0] * d[0] + d[1] * d[1])


def rect_area(roi_):
	return roi_[2] * roi_[3]


def is_neighbor_distance(obj_, dist_):
        return dist_ < TRACK_DISTANCE_THRESHOLD * obj_._radius


def f(state, noise):
	return state + np.sin(noise)


def g(state, noise):
	return state + np.cos(noise)
