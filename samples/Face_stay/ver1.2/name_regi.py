import os
import sys
import shutil
import piexif
import piexif.helper
from data_collector import *
from face_collector import *

COLLECT_SAVE_LOGS = True
NAME_PATH = 'aws_img/name'
ENTER_PATH = 'aws_img/enter'
EXIT_PATH = 'aws_img/exit'

if __name__ == '__main__':
    data_collect = data_collector(COLLECT_SAVE_LOGS)
    face_collect = face_collector(COLLECT_SAVE_LOGS)

    imgpath = sys.argv[1]
    name = sys.argv[2]

    if not os.path.isdir(NAME_PATH):
        os.makedirs(NAME_PATH)

    if os.path.exists(imgpath):
        (_, imgname) = imgpath.rsplit('/', 1)
    #    shutil.copyfile(imgpath, NAME_PATH + '/' + imgname)
    #    piexif.remove(NAME_PATH + '/' + imgname)
    #    usercomment = piexif.helper.UserComment.dump(name, 'unicode')
    #    exif_ifd = {piexif.ExifIFD.UserComment: usercomment}
    #    exif_dict = {"Exif":exif_ifd}
    #    exif_bytes = piexif.dump(exif_dict)
    #    piexif.insert(exif_bytes, NAME_PATH + '/' + imgname)

    else:
        print('Images is not found.')
        quit()

    (faceid, _) = imgname.rsplit('.', 1)
    faceid = int(faceid)

    if os.path.exists(ENTER_PATH + '/' + imgname):
        exif_dict = piexif.load(ENTER_PATH + '/' + imgname)
        entertime = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode(encoding='utf-8')
        entertime = entertime.replace(" ", "T")
        usercomment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
        usercomment = usercomment.split(':')
        ageave = int(usercomment[0])
        agewidth = int(usercomment[1])
        gender = usercomment[2]
    else:
        entertime = "-"
        ageave = 0
        agewidth = 0
        gender = "-"

    if os.path.exists(EXIT_PATH + '/' + imgname):
        exif_dict = piexif.load(EXIT_PATH + '/' + imgname)
        exittime = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode(encoding='utf-8')
        exittime = exittime.replace(" ", "T")
    else:
        exittime = "-"
   
    data_collect.data_input(faceid, name, entertime, exittime, ageave, agewidth, gender)
    face_collect.face_upload(faceid, imgpath, name)

    # Copy face image
    shutil.copyfile(imgpath, NAME_PATH + '/' + imgname)
    piexif.remove(NAME_PATH + '/' + imgname)
    usercomment = piexif.helper.UserComment.dump(name, 'unicode')
    exif_ifd = {piexif.ExifIFD.UserComment: usercomment}
    exif_dict = {"Exif":exif_ifd}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, NAME_PATH + '/' + imgname)
