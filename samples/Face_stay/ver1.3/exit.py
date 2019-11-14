import scorer
import time
import threading
from video_capturer import *
from face_detector import *
from object_tracker import *
from face_indexer import *
from data_collector import *

# Debugging output control
MV_TRACK_ENDURANCE_THRESHOLD = 3
MV_TRACK_MATURITY_THRESHOLD = 1
MV_TRACK_AFTER_A_MOMENT_TIME = 1
MV_TRACK_WANDERER_EPSILON = 0.01

# Output control
DETECT_SAVE_LOGS = True
TRACK_SAVE_LOGS = True
TRACK_SAVE_SNAPSHOTS = True
TRACK_IMSHOW = True
TRACK_SHARPENING4 = False
TRACK_SHARPENING8 = False
INDEX_SAVE_LOGS = True
INDEX_SAVE_SNAPSHOTS = True
INDEX_IMSHOW = False
DATA_SAVE_LOGS = True

def lost(face_index, data_collect, lost_list):
    face_index.face_search_exit(lost_list)
    for value in face_index.result():
        data_collect.exit_data_input(value[0], value[1])

if __name__ == '__main__':
    threads = []
    video_capture = video_capturer("scorer")
    face_detect = face_detector(DETECT_SAVE_LOGS)
    object_track = object_tracker(TRACK_SAVE_LOGS, TRACK_SAVE_SNAPSHOTS, TRACK_IMSHOW, TRACK_SHARPENING4, TRACK_SHARPENING8,
            MV_TRACK_ENDURANCE_THRESHOLD, MV_TRACK_MATURITY_THRESHOLD, MV_TRACK_AFTER_A_MOMENT_TIME, MV_TRACK_WANDERER_EPSILON)
    face_index = face_indexer(INDEX_SAVE_LOGS, INDEX_SAVE_SNAPSHOTS, INDEX_IMSHOW)
    data_collect = data_collector(DATA_SAVE_LOGS)

    try:
        while True:
            face_detect.detect(*video_capture.get_image())
            object_track.track_objects(*face_detect.result())
            if len(object_track.result()) > 0:
                thread_lost = threading.Thread(target=lost, args=(face_index, data_collect, object_track.result(),))
                threads.append(thread_lost)
                thread_lost.start()
    except KeyboardInterrupt:
        print('Stop')
