import scorer
import time
import threading
from face_detector import *
from object_tracker import *
from face_indexer import *

# Debugging output control
MV_TRACK_ENDURANCE_THRESHOLD = 3
MV_TRACK_MATURITY_THRESHOLD = 1
MV_TRACK_AFTER_A_MOMENT_TIME = 1
MV_TRACK_WANDERER_EPSILON = 0.01

# Output control
DETECT_SAVE_LOGS = True
TRACK_SAVE_LOGS = True
TRACK_SAVE_SNAPSHOTS = True
TRACK_IMSHOW = False
TRACK_SHARPENING4 = False
TRACK_SHARPENING8 = False
INDEX_SAVE_LOGS = True
INDEX_SAVE_SNAPSHOTS = True
INDEX_IMSHOW = True

def lost(face_index, lost_list):
	face_index.face_search_exit(lost_list)

if __name__ == '__main__':
	threads = []
	face_detect = face_detector(DETECT_SAVE_LOGS)
	object_track = object_tracker(TRACK_SAVE_LOGS, TRACK_SAVE_SNAPSHOTS, TRACK_IMSHOW, TRACK_SHARPENING4, TRACK_SHARPENING8,
			MV_TRACK_ENDURANCE_THRESHOLD, MV_TRACK_MATURITY_THRESHOLD, MV_TRACK_AFTER_A_MOMENT_TIME, MV_TRACK_WANDERER_EPSILON)
	face_index = face_indexer(INDEX_SAVE_LOGS, INDEX_SAVE_SNAPSHOTS, INDEX_IMSHOW)
	if not face_index.collection_check():
		reko.collection_create()

	try:
		while True:
			face_detect.detect()
			object_track.track_objects(*face_detect.result())
			if len(object_track.result()) > 0:
				thread_lost = threading.Thread(target=lost, args=(face_index, object_track.result(),))
				threads.append(thread_lost)
				thread_lost.start()
			#face_index.face_search_exit(object_track.result())
	except KeyboardInterrupt:
		print('Stop')
