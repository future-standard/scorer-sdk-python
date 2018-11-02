from face_detector import *
from object_tracker import *

# Debugging output control
MV_TRACK_ENDURANCE_THRESHOLD = 3
MV_TRACK_MATURITY_THRESHOLD = 1
MV_TRACK_AFTER_A_MOMENT_TIME = 2
MV_TRACK_WANDERER_EPSILON = 0.01

# Log and snapshot output control
DETECT_SAVE_LOGS = True
TRACK_SAVE_LOGS = True
TRACK_SAVE_SNAPSHOTS = True
TRACK_IMSHOW = True
TRACK_SHARPENING4 = False
TRACK_SHARPENING8 = False


if __name__ == '__main__':
	face_detect = face_detector(DETECT_SAVE_LOGS)
	object_track = object_tracker(TRACK_SAVE_LOGS, TRACK_SAVE_SNAPSHOTS, TRACK_IMSHOW, TRACK_SHARPENING4, TRACK_SHARPENING8, 
				MV_TRACK_ENDURANCE_THRESHOLD, MV_TRACK_MATURITY_THRESHOLD, MV_TRACK_AFTER_A_MOMENT_TIME, MV_TRACK_WANDERER_EPSILON)

	try:
		while True:
			face_detect.detect()
			object_track.track_objects(*face_detect.result())
	except KeyboardInterrupt:
		print('Stop')
