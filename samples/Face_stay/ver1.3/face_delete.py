import os
import shutil
from face_indexer import *
from data_collector import *
from datetime import datetime

# Log and snapshot output control
INDEX_SAVE_LOGS = True
INDEX_SAVE_SNAPSHOTS = False
INDEX_IMSHOW = False
DATA_SAVE_LOGS = True

NAME_IMG_PATH = 'aws_img/name'
ENTER_IMG_PATH = 'aws_img/enter'
EXIT_IMG_PATH = 'aws_img/exit'

if __name__ == '__main__':
    face_index = face_indexer(INDEX_SAVE_LOGS, INDEX_SAVE_SNAPSHOTS, INDEX_IMSHOW)
    face_index.face_delete_all()

    data_collect = data_collector(DATA_SAVE_LOGS)
    data_collect.table_delete()

    time = datetime.now().strftime("%Y%m%d%H%M%S")

    if not os.path.isdir(NAME_IMG_PATH + '/old'):
        os.makedirs(NAME_IMG_PATH + '/old')

    if not os.path.isdir(ENTER_IMG_PATH + '/old'):
        os.makedirs(ENTER_IMG_PATH + '/old')

    if not os.path.isdir(EXIT_IMG_PATH + '/old'):
        os.makedirs(EXIT_IMG_PATH + '/old')

    if not os.path.isdir(NAME_IMG_PATH + '/old/' + time):
        os.makedirs(NAME_IMG_PATH + '/old/' + time)

    if not os.path.isdir(ENTER_IMG_PATH + '/old/' + time):
        os.makedirs(ENTER_IMG_PATH + '/old/' + time)

    if not os.path.isdir(EXIT_IMG_PATH + '/old/' + time):
        os.makedirs(EXIT_IMG_PATH + '/old/' + time)

    for file in glob.glob(NAME_IMG_PATH + '/*.jpg'):
        if os.path.isfile(file):
            shutil.move(file, file.replace('name/', 'name/old/' + time + '/'))

    for file in glob.glob(ENTER_IMG_PATH + '/*.jpg'):
        if os.path.isfile(file):
            shutil.move(file, file.replace('enter/', 'enter/old/' + time + '/'))

    for file in glob.glob(EXIT_IMG_PATH + '/*.jpg'):
        if os.path.isfile(file):
            shutil.move(file, file.replace('exit/', 'exit/old/' + time + '/'))
