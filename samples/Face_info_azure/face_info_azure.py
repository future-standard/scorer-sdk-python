import scorer
import cv2
import numpy as np
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import json
import logging
import os

IMG_PATH = 'azure_img/'
LOG_PATH = 'azure/'
FACE_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
FACE_SEARCH_THRESHOLD = 2
CUT_WIDTH_MARGIN = 20
CUT_HEIGHT_MARGIN = 40
FACE_MINIMUM_SIZE = 30

headers = {
	'Content-Type': 'application/octet-stream',
	'Ocp-Apim-Subscription-Key': FACE_API_KEY,
}


params = urllib.parse.urlencode({
	'returnFaceId': 'true',
	'returnFaceAttributes': 'age,gender'
})


class face_info_azure:
	def __init__(self, save_logs_, save_snapshots_, imshow_):
		self._conn = None
		self._save_logs = save_logs_
		self._save_snapshots = save_snapshots_
		self._imshow = imshow_
		self._imshow_list = []
		self._imshow_num = 1

		if not os.path.isdir(LOG_PATH):
			os.makedirs(LOG_PATH)
		if not os.path.isdir(IMG_PATH):
			os.makedirs(IMG_PATH)

		# Log
		self._azure_logger = logging.getLogger('azure_log')
		self._azure_logger.setLevel(10)
		azure_log = logging.FileHandler('azure/face_api.log')
		self._azure_logger.addHandler(azure_log)
		azure_stream = logging.StreamHandler()
		self._azure_logger.addHandler(azure_stream)	


	def conn_open(self):
		if self._conn == None:
			self._conn = http.client.HTTPSConnection('japaneast.api.cognitive.microsoft.com')
		else:
			print('Azure already connected')


	def face_info(self, objs):
		for obj in objs:
			if (obj._last_seen - obj._start).total_seconds() > FACE_SEARCH_THRESHOLD:
				# Cut face
				cut_size = np.array([int(obj._roi2[0]) - CUT_WIDTH_MARGIN, int(obj._roi2[0]) + int(obj._roi2[2]) + CUT_WIDTH_MARGIN,
				int(obj._roi2[1]) - CUT_HEIGHT_MARGIN, int(obj._roi2[1]) + int(obj._roi2[3]) + CUT_HEIGHT_MARGIN])
				cut_size[cut_size < 0] = 0
				if (cut_size[2] - cut_size[3]) * (cut_size[0] - cut_size[1]) > FACE_MINIMUM_SIZE:
					dst = obj._snapshot2[cut_size[2]:cut_size[3], cut_size[0]:cut_size[1]]

					# Convert ndarray to bytearray
					ret, data = cv2.imencode('.png', dst)
					imgbytes = bytearray(data)

					self._conn.request("POST", "/face/v1.0/detect?%s" % params, imgbytes, headers)
					response = self._conn.getresponse()

					try:
						data = json.loads(response.read().decode('utf-8'))
						self._azure_logger.log(20, data)
						age = data[0]['faceAttributes']['age']
						gender = data[0]['faceAttributes']['gender']
						text1 = 'Age:' + str(age)
						text2 = 'Gender:' + str(gender)
						cv2.putText(dst, text1, (5, dst.shape[1] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
						cv2.putText(dst, text2, (5, dst.shape[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

						if self._save_snapshots:
							cv2.imwrite(IMG_PATH + str(obj._object_id) + '.png', dst)
						if self._imshow:
							self.face_imshow_update(dst)

					except:
						self._reko_logger.log(20, traceback.format_exc())
						print('target: ' + str(obj._object_id) + ' is not face!')

		if self._imshow:
			self.face_imshow()


	def conn_close(self):
		if self._conn != None:
			self._conn.close()
		else:
			print('Connection is not found')


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
