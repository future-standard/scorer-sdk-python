import os
import boto3
import json
import piexif
import logging
from botocore.exceptions import ClientError

AWS_LOG_PATH = 'aws/'
LOG_PATH = 'log/'
NAME_PATH = 'aws_img/name/'
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxx'
AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxx'
BUCKET_NAME = 'scorer-room'


class face_collector:
    def __init__(self, save_logs_):
        # Create Client
        self._client = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = "ap-northeast-1")
        # Create Bucket
        self._bucket = self._client.Bucket(BUCKET_NAME)
        self._save_logs = save_logs_

        if self._save_logs:
            self._s3_logger = logging.getLogger('s3_log')
            self._s3_logger.setLevel(10)
            s3_log = logging.FileHandler(AWS_LOG_PATH + 's3.log')
            self._s3_logger.addHandler(s3_log)
            s3_stream = logging.StreamHandler()
            self._s3_logger.addHandler(s3_stream)


    def face_upload(self, faceid, imgpath, username):
        # Delete old face image
        if os.path.exists(NAME_PATH + str(faceid) + '.jpg'):
            exif_dict = piexif.load(NAME_PATH + str(faceid) + '.jpg')
            name = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
            #print(name)
            response = self._bucket.delete_objects(
                Delete={
                    'Objects': [
                        {'Key': name + '.jpg',},
                    ],
                },
            )
            if self._save_logs:
                self._s3_logger.log(20, str(response))

        # Upload new face image
        self._bucket.upload_file(imgpath, username + '.jpg')
            

#if __name__ == '__main__':
#     face_collect = face_collector(True)
#     face_collect.face_upload('aws_img/name/1.jpg', '鳥海')
