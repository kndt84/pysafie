import json
from datetime import datetime, timedelta
import requests
import json
import boto3


class Safie:

    def __init__(self, client_id, client_secret, username, password, dynamodb_table):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(dynamodb_table)

    def create_access_token(self):
        url = 'https://app.safie.link/auth/authorize'
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'jobType': 'Period',
            'scope': 'use'
        }
        res = requests.post(url, data=payload)
        return json.loads(res.text)

    def refresh_access_token(self, refresh_token):
        url = 'https://app.safie.link/auth/token'
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'scope': 'use'
        }
        res = requests.post(url, data=payload)
        return json.loads(res.text)

    def create_media_download_request(self, access_token, device_id, start, end):
        url = 'https://app.safie.link/api/media/download/request'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        payload = {
            'deviceid': device_id,
            'start': start,
            'end': end
        }
        res = requests.post(url, data=payload, headers=headers)
        return json.loads(res.text)

    def get_media_download_request_list(self, access_token, device_id):
        url = 'https://app.safie.link/api/media/download/list'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        payload = {
            'deviceid': device_id
        }
        res = requests.get(url, data=payload, headers=headers)
        return json.loads(res.text)

    def get_media_download_request_status(self, access_token, device_id, request_id):
        url = 'https://app.safie.link/api/media/download/status'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        payload = {
            'requestid': request_id,
            'deviceid': device_id
        }
        res = requests.get(url, data=payload, headers=headers)
        return json.loads(res.text)

    def delete_media_download_request(self, access_token, device_id, request_id):
        url = 'https://app.safie.link/api/media/download/delete'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        payload = {
            'requestid': request_id,
            'deviceid': device_id
        }
        res = requests.post(url, data=payload, headers=headers)
        return json.loads(res.text)

    def save_access_token(self, auth_info):
        auth_info['username'] = self.username
        auth_info['issued_at'] = int(datetime.now().timestamp())
        auth_info['expires_at'] = int(
            datetime.now().timestamp()) + auth_info['expires_in']
        return self.table.put_item(Item=auth_info)

    def get_access_token(self):
        return self.table.get_item(Key={'username': self.username})['Item']
