import boto3
import numpy as np
import cv2
import scorer
import datetime
import glob
import traceback
import logging
import os
from tracked_object import *
from botocore.exceptions import ClientError

AWS_LOG_PATH = 'aws/'
INFO_PATH = 'aws_img/info/'
COLLECTION_ID = 'test'
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxxxx'
AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
MAX_RESULTS = 20
CUT_WIDTH_MARGIN = 20
CUT_HEIGHT_MARGIN = 40
FACE_MINIMUM_SIZE = 30
FACE_SEARCH_THRESHOLD = 2
#FACE_DELETE_THRESHOLD = 1800
#MIN_FACE_MATCH_THRESHOLD = 95


class face_info_aws:
	def __init__(self, save_logs_, save_snapshots_, imshow_):
		# Create Client
		self._client = boto3.client('rekognition', aws_access_key_id = AWS_ACCESS_KEY_ID, 
				aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = "ap-northeast-1")
		self._imshow_list = []
		self._imshow_num = 1
		self._save_logs = save_logs_
		self._save_snapshots = save_snapshots_
		self._imshow = imshow_

		if not os.path.isdir('aws_img/'):
			os.makedirs('aws_img/')
		if not os.path.isdir(AWS_LOG_PATH):
			os.makedirs(AWS_LOG_PATH)
		if not os.path.isdir(INFO_PATH):
			os.makedirs(INFO_PATH)

		if self._save_logs:
			self._reko_logger = logging.getLogger('reko_log')
			self._reko_logger.setLevel(10)
			reko_log = logging.FileHandler(AWS_LOG_PATH + 'rekognition.log')
			self._reko_logger.addHandler(reko_log)
			reko_stream = logging.StreamHandler()
			self._reko_logger.addHandler(reko_stream)


	def collection_check(self):
		response = self._client.list_collections(MaxResults = MAX_RESULTS)
		collections = response['CollectionIds']

		if self._save_logs:
			if not COLLECTION_ID in collections:
				self._reko_logger.log(20, 'The collection ' + COLLECTION_ID + ' was not found ')
			else:
				self._reko_logger.log(20, 'The collection ' + COLLECTION_ID + ' was found ')

		return COLLECTION_ID in collections


	def collection_create(self):
		response = self._client.create_collection(CollectionId = COLLECTION_ID)
		if self._save_logs:
			self._reko_logger.log(20, 'Creating collection:' + COLLECTION_ID)
			self._reko_logger.log(20, 'Collection ARN: ' + response['CollectionArn'])
			self._reko_logger.log(20, 'Status code: ' + str(response['StatusCode']))
			self._reko_logger.log(20, 'Done...')


	def collection_delete(self):
		try:
			response = self._client.delete_collection(CollectionId = COLLECTION_ID)
			statusCode = response['StatusCode']

		except ClientError as e:
			if self._save_logs:
				if e.response['Error']['Code'] == 'ResourceNotFoundException':
					self._reko_logger.log(20, 'The collection ' + COLLECTION_ID + ' was not found ')
				else:
					self._reko_logger.log(20, 'Error other than Not Found occurred: ' + e.response['Error']['Message'])
			statusCode=e.response['ResponseMetadata']['HTTPStatusCode']

		if self._save_logs:
			self._reko_logger.log(20, 'Operation returned Status Code: ' + str(statusCode))
			self._reko_logger.log(20, 'Done...')


	def face_info(self, objs):
		for obj in objs:
			if (obj._last_seen - obj._start).total_seconds() > FACE_SEARCH_THRESHOLD:
				# Cut face and save
				cut_size = np.array([int(obj._roi2[0]) - CUT_WIDTH_MARGIN, int(obj._roi2[0]) + int(obj._roi2[2]) + CUT_WIDTH_MARGIN,
						int(obj._roi2[1]) - CUT_HEIGHT_MARGIN, int(obj._roi2[1]) + int(obj._roi2[3]) + CUT_HEIGHT_MARGIN])
				cut_size[cut_size < 0] = 0
				if (cut_size[2] - cut_size[3]) * (cut_size[0] - cut_size[1]) > FACE_MINIMUM_SIZE:
					dst = obj._snapshot2[cut_size[2]:cut_size[3], cut_size[0]:cut_size[1]]

					# Convert ndarray to bytearray
					ret, data = cv2.imencode('.png', dst)
					imgbytes = bytearray(data)

					# Detect face
					try:
						response = self._client.detect_faces(Image={'Bytes': imgbytes}, Attributes=['ALL'])
						if self._save_logs:
							self._reko_logger.log(20, response)
						facedetails = response['FaceDetails'][0]
						highage = facedetails['AgeRange']['High']
						lowage = facedetails['AgeRange']['Low']
						age_ave = (highage + lowage)/2
						age_width = abs((highage - lowage)/2)
						gender = facedetails['Gender']['Value']

						text1 = 'Age: ' + str(age_ave) + '+-' + str(age_width)
						text2 = 'Gender: ' + str(gender)
						cv2.putText(dst, text1, (5, dst.shape[1] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
						cv2.putText(dst, text2, (5, dst.shape[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

						if self._save_snapshots:
							cv2.imwrite(INFO_PATH + str(obj._object_id) + '.png', dst)
						if self._imshow:
							self.face_imshow_update(dst)

					except:
						self._reko_logger.log(20, traceback.format_exc())
						print('target:' + str(obj._object_id) + 'is not face!')

		if self._imshow:
			self.face_imshow()


	def face_imshow_update(self, dst):
		if self._imshow_num > len(self._imshow_list) and len(self._imshow_list) < 5:
			self._imshow_list.append(dst)
		else:
			self._imshow_list[self._imshow_num - 1] = dst

		if self._imshow_num == 4:
			self._imshow_num = 1
		else:
			self._imshow_num += 1


	def face_imshow(self):
		try:
			scorer.imshow(1, self._imshow_list[0])
			scorer.imshow(2, self._imshow_list[1])
			scorer.imshow(3, self._imshow_list[2])
			scorer.imshow(4, self._imshow_list[3])
		except:
			pass
