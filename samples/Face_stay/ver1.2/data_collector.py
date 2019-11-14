import boto3
import json
import decimal
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

COLLECT_SAVE_LOGS = True

AWS_LOG_PATH = 'aws/'
LOG_PATH = 'log/'
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxxx' 
AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxx'
TABLE_NAME = 'ScorerRoom'

class data_collector:
	def __init__(self, save_logs_):
		#Create Client
		self._client = boto3.resource('dynamodb', aws_access_key_id = AWS_ACCESS_KEY_ID,
                                aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = "ap-northeast-1")
		self._table = None
		self._save_logs = save_logs_

		if self._save_logs:
                        self._db_logger = logging.getLogger('db_log')
                        self._db_logger.setLevel(10)
                        db_log = logging.FileHandler(AWS_LOG_PATH + 'dynamodb.log')
                        self._db_logger.addHandler(db_log)
                        db_stream = logging.StreamHandler()
                        self._db_logger.addHandler(db_stream)

		self.table_check()


	def table_check(self):
		try:
			response = self.table_create()
			print('Table is created.')
			
		except ClientError as e:
			self._table = self._client.Table(TABLE_NAME)
			#print(e.response['Error']['Message'])
			if self._save_logs:
				self._db_logger.log(20, e.response['Error']['Message'])


	def table_create(self):
		self._table = self._client.create_table(
			TableName = TABLE_NAME,
			KeySchema = [
				{
					'AttributeName': 'faceid',
					'KeyType': 'HASH'
				},
			],
			AttributeDefinitions = [
				{
					'AttributeName': 'faceid',
					'AttributeType': 'N'
				},
			],
			ProvisionedThroughput = {
				'ReadCapacityUnits': 10,
				'WriteCapacityUnits': 10
			}
		)


	def table_delete(self):
		response = self._table.delete()
		print('Table is deleted.')
		if self._save_logs:
			self._db_logger.log(20, str(response))


	def data_input(self, faceid, username, entertime, exittime, ageave, agewidth, gender):
		# Search Data
		response = self._table.query(KeyConditionExpression = Key('faceid').eq(faceid))
		if self._save_logs:
			self._db_logger.log(20, str(response))

		# Input Data
		if not response['Items']:
			response = self._table.put_item(
				Item = {
					'faceid': faceid,
					'username': username,
					'entertime': entertime,
					'exittime': exittime,
					'ageave': ageave,
					'agewidth': agewidth,
					'gender': gender,
				}
			)
			print(response)
			if self._save_logs:
				self._db_logger.log(20, str(response))
		else:
			response = self._table.update_item(
				Key = {
					'faceid': faceid
				},
				UpdateExpression = 'set username = :name, entertime = :enter, exittime = :exit, ageave = :ageave, agewidth = :agewidth, gender = :gender',
				ExpressionAttributeValues = {
                                        ':name': username,
					':enter': entertime,
                                        ':exit': exittime,
					':ageave': ageave,
					':agewidth': agewidth,
					':gender': gender
				},
				ReturnValues = "UPDATED_NEW"
			)
			if self._save_logs:
				self._db_logger.log(20, str(response))


	def enter_data_input(self, faceid, entertime, ageave, agewidth, gender):
		response = self._table.query(KeyConditionExpression = Key('faceid').eq(faceid))
		if self._save_logs:
			self._db_logger.log(20, str(response))

		if not response['Items']:
			response = self._table.put_item(
				Item = {
					'faceid': faceid,
					'username': '-',
					'entertime': entertime,
					'exittime': '-',
					'ageave': ageave,
					'agewidth': agewidth,
					'gender': gender,
				}
			)
			#print(response)
			if self._save_logs:
				self._db_logger.log(20, str(response))
		else:
			response = self._table.update_item(
				Key = {
					'faceid': faceid
				},
				UpdateExpression = 'set entertime = :enter, ageave = :ageave, agewidth = :agewidth, gender = :gender',
				ExpressionAttributeValues = {
					':enter': entertime,
					':ageave': ageave,
					':agewidth': agewidth,
					':gender': gender
				},
				ReturnValues = "UPDATED_NEW"
			)
			if self._save_logs:
				self._db_logger.log(20, str(response))


	def exit_data_input(self, faceid, exittime):
		response = self._table.query(KeyConditionExpression = Key('faceid').eq(faceid))

		if self._save_logs:
			self._db_logger.log(20, str(response))

		if response['Items']:
			response = self._table.update_item(
				Key = {
					'faceid': faceid
				},
				UpdateExpression='set exittime = :exit',
				ExpressionAttributeValues = {
					':exit': exittime
				},
				ReturnValues = "UPDATED_NEW"
			)
			if self._save_logs:
				self._db_logger.log(20, str(response))


#if __name__ == '__main__':
#	data_collect = data_collector(COLLECT_SAVE_LOGS)
#	data_collect.data_input(3, 'Taiki', '2019-03-29T14:25:00', '2019-03-30T14:26:00', 25, 3, 'Female')
#	data_collect.table_delete()
