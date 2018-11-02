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
LOG_PATH = 'log/'
IMG_PATH = 'aws_img/regist/'
TIME_PATH = 'aws_img/timestamp/'
#INFO_PATH = 'aws_img/info/'
COLLECTION_ID = 'test'
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxxxxxxxx'
AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxx'
MAX_RESULTS = 20
CUT_WIDTH_MARGIN = 20
CUT_HEIGHT_MARGIN = 40
FACE_MINIMUM_SIZE = 30
FACE_SEARCH_THRESHOLD = 2
FACE_DELETE_THRESHOLD = 1800
MIN_FACE_MATCH_THRESHOLD = 95


class face_indexer:
	def __init__(self, save_logs_, save_snapshots_, imshow_):
		# Create Client
		self._client = boto3.client('rekognition', aws_access_key_id = AWS_ACCESS_KEY_ID, 
				aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = "ap-northeast-1")
		self._objectid = self.objectid_set()
		self._faces = {}
		self._imshow_list = []
		self._imshow_num = 1
		self._save_logs = save_logs_
		self._save_snapshots = save_snapshots_
		self._imshow = imshow_

		if not os.path.isdir('aws_img/'):
			os.makedirs('aws_img/')
		if not os.path.isdir(AWS_LOG_PATH):
			os.makedirs(AWS_LOG_PATH)
		if not os.path.isdir(LOG_PATH):
			os.makedirs(LOG_PATH)
		if not os.path.isdir(IMG_PATH):
			os.makedirs(IMG_PATH)
		if not os.path.isdir(TIME_PATH):
			os.makedirs(TIME_PATH)

		if self._save_logs:
			self._reko_logger = logging.getLogger('reko_log')
			self._reko_logger.setLevel(10)
			reko_log = logging.FileHandler(AWS_LOG_PATH + 'rekognition.log')
			self._reko_logger.addHandler(reko_log)
			reko_stream = logging.StreamHandler()
			self._reko_logger.addHandler(reko_stream)

			self._regi_logger = logging.getLogger('regi_log')
			self._regi_logger.setLevel(10)
			regi_log = logging.FileHandler(LOG_PATH + 'registration.log')
			self._regi_logger.addHandler(regi_log)
			regi_stream = logging.StreamHandler()
			self._regi_logger.addHandler(regi_stream)


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

	
	def face_add(self, obj, objectid):
		t = obj._last_seen
		ext_id = None
		imgname = None
		if objectid == None:
			ext_id = '%d_img:%04d:%02d:%02d:%02d:%02d:%02d' % (self._objectid, t.year, t.month, t.day, t.hour, t.minute, t.second)
			imgname = IMG_PATH + str(self._objectid) + '.png'
			self._objectid += 1
		else:
			ext_id = '%d_img:%04d:%02d:%02d:%02d:%02d:%02d' % (objectid, t.year, t.month, t.day, t.hour, t.minute, t.second)
			imgname = IMG_PATH + str(objectid) + '.png'

		# Cut face and save
		cut_size = np.array([int(obj._roi2[0]) - CUT_WIDTH_MARGIN, int(obj._roi2[0]) + int(obj._roi2[2]) + CUT_WIDTH_MARGIN,
					int(obj._roi2[1]) - CUT_HEIGHT_MARGIN, int(obj._roi2[1]) + int(obj._roi2[3]) + CUT_HEIGHT_MARGIN])
		cut_size[cut_size < 0] = 0
		if (cut_size[2] - cut_size[3]) * (cut_size[0] - cut_size[1]) > FACE_MINIMUM_SIZE:
			dst = obj._snapshot2[cut_size[2]:cut_size[3], cut_size[0]:cut_size[1]]

			# Convert ndarray to bytearray
			ret, data = cv2.imencode('.png', dst)
			imgbytes = bytearray(data)

			# Send face
			response = self._client.index_faces(CollectionId = COLLECTION_ID, DetectionAttributes = [], 
									ExternalImageId = ext_id, Image={'Bytes': imgbytes})

			if self._save_logs:
				self._reko_logger.log(20, str(response))
				for faceRecord in response['FaceRecords']:
					self._regi_logger.log(20, 'add:' + str(faceRecord['Face']['FaceId']) + ' ' + str(faceRecord['Face']['ExternalImageId']))

			if objectid == None:
				self._faces[str(self._objectid - 1)] = obj
			else:
				self._faces[str(objectid)] = obj

			if self._save_snapshots:
				cv2.imwrite(imgname, dst)
			if self._imshow:
				self.face_imshow_update(dst)


	def face_search_out(self, objs):
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

					# Face search
					try:
						response = self._client.search_faces_by_image(CollectionId = COLLECTION_ID, Image={'Bytes': imgbytes},
									FaceMatchThreshold = MIN_FACE_MATCH_THRESHOLD, MaxFaces = MAX_RESULTS)
						faceMatches = response['FaceMatches']

						if len(faceMatches) > 0:
							similarity = 0
							objectid = ''
							for match in faceMatches:
								if match['Similarity'] > similarity:
									similarity = match['Similarity']
									tmp = match['Face']['ExternalImageId'].split(':')
									objectid = int(tmp.pop(0).split('_')[0])
									tmp = [int(t) for t in tmp]
									time = datetime.datetime(*tmp)

							if self._save_logs:
								self._regi_logger.log(20, 'detect:' + str(objectid) + ' enter:' + str(time) + ' out:' + str(obj._last_seen))

							text1 = 'Faceid: ' + str(objectid)
							text2 = 'Enter: ' + str(time.time())
							text3 = 'Out: ' + str(obj._last_seen.time())
							cv2.putText(dst, text1, (5, dst.shape[1] - 60),
									cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
							cv2.putText(dst, text2, (5, dst.shape[1] - 40),
									cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
							cv2.putText(dst, text3, (5, dst.shape[1] - 20),
									cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

							if self._save_snapshots:
								cv2.imwrite(TIME_PATH + str(objectid) + '.png', dst)
							if self._imshow:
								self.face_imshow_update(dst)

					except:
						self._reko_logger.log(20, traceback.format_exc())
						print('target: ' + str(obj._object_id) + ' is not face!')
		if self._imshow:
			self.face_imshow()


	def face_search_enter(self, objs):
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

					# Face search
					try:
						response = self._client.search_faces_by_image(CollectionId = COLLECTION_ID, Image={'Bytes': imgbytes}, 
										FaceMatchThreshold = MIN_FACE_MATCH_THRESHOLD, MaxFaces = MAX_RESULTS)

						if self._save_logs:
							self._reko_logger.log(20, response)

						faceMatches = response['FaceMatches']

						if len(faceMatches) > 0:
							self.old_face_delete()
							self.face_update(obj, response)
						else:
							self.old_face_delete()
							self.face_add(obj, None)
					except:
						self._reko_logger.log(20, traceback.format_exc())
						print('target:' + str(obj._object_id) + 'is not face!')
		if self._imshow:
			self.face_imshow()


	def face_update(self, obj, response):
		delete_faceid = [""]
		similarity = 0
		objectid = 0
		faceMatches = response['FaceMatches']

		for match in faceMatches:
			if match['Similarity'] > similarity:
				delete_faceid = [match['Face']['FaceId']]
				similarity = match['Similarity']
				tmp = match['Face']['ExternalImageId'].split(':')
				objectid = int(tmp.pop(0).split('_')[0])

		old_area = self._faces[str(objectid)]._roi2[2] * self._faces[str(objectid)]._roi2[3]
		new_area = obj._roi2[2] * obj._roi2[3]
		if new_area > old_area:
			self.face_add(obj, objectid)
			self.face_delete(delete_faceid)
		else:
			print('The area of the new face is smaller')


	def old_face_delete(self):
		response = self._client.list_faces(CollectionId = COLLECTION_ID, MaxResults = MAX_RESULTS)
		faces = response['Faces']
		delete_faceids = []

		for face in faces:
			tmp = face['ExternalImageId'].split(':')
			objectid = int(tmp.pop(0).split('_')[0])
			tmp = [int(t) for t in tmp]
			update_time = datetime.datetime(*tmp)
			diff_time = (datetime.datetime.now() - update_time).total_seconds()
			if diff_time > FACE_DELETE_THRESHOLD:
				delete_faceids.append(face['FaceId'])
		if len(delete_faceids) > 0:
			self.face_delete(delete_faceids)
	

	def face_delete_all(self):
		response = self._client.list_faces(CollectionId = COLLECTION_ID, MaxResults = MAX_RESULTS)

		while True:
			faces = response['Faces']
			faceids = []

			for face in faces:
				faceids.append(face['FaceId'])
			
			self.face_delete(faceids)

			if 'NextToken' in response:
				nextToken = response['NextToken']
				response = self._client.list_faces(CollectionId = COLLECTION_ID, NextToken = nextToken, MaxResults = MAX_RESULTS)
			else:
				break


	def face_delete(self, faceids):
		if len(faceids) > 0:
			response = self._client.delete_faces(CollectionId = COLLECTION_ID, FaceIds = faceids)
			if self._save_logs:
				self._reko_logger.log(20, response)
				for faceId in response['DeletedFaces']:
					self._regi_logger.log(20, 'delete:' + faceId)
		else:
			self._reko_logger.log(20, 'Face Ids were not found')


	def objectid_set(self):
		objectid = 0
		for file in glob.glob(IMG_PATH + "*"):
			try:
				id = int(file.strip(IMG_PATH).strip('.png'))
				if id > objectid:
					objectid = id
			except:
				pass
		return (objectid + 1)


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
