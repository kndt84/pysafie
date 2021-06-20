import requests
import json
import time


BASE_URL = 'https://openapi.safie.link'


class Safie:

    def __init__(self, client_id, client_secret, redirect_uri,
                 access_token=None, refresh_token=None, expires_at=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    # Auth APIs
    def get_access_token(self, authorization_code):
        url = '{}/v1/auth/token'.format(BASE_URL)
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'code': authorization_code
        }
        res = requests.post(url, data=payload)
        d = json.loads(res.text)
        print(d)
        self.access_token = d['access_token']
        self.refresh_token = d['refresh_token']
        self.expires_at = int(time.time()) + d['expires_in']
        return res

    def refresh_access_token(self):
        url = '{}/v1/auth/refresh-token'.format(BASE_URL)
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'scope': 'safie-api'
        }
        res = requests.post(url, data=payload)
        d = json.loads(res.text)
        self.access_token = d['access_token']
        self.refresh_token = d['refresh_token']
        self.expires_at = int(time.time()) + d['expires_in']
        return res

    # Media file APIs
    def get_media_file_request_list(self, device_id):
        url = '{}/v1/devices/{}/media_files/requests'.format(
            BASE_URL, device_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        return requests.get(url, headers=headers)

    def create_media_file_request(self, device_id, start_datetime, end_datetime):
        start = start_datetime.strftime('%Y-%m-%dT%H:%M:%S+0900')
        end = end_datetime.strftime('%Y-%m-%dT%H:%M:%S+0900')
        url = '{}/v1/devices/{}/media_files/requests'.format(
            BASE_URL, device_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        payload = {
            'start': start,
            'end': end
        }
        return requests.post(url, data=json.dumps(payload), headers=headers)

    def get_media_file_request(self, device_id, request_id):
        url = '{}/v1/devices/{}/media_files/requests/{}'.format(
            BASE_URL, device_id, request_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        return requests.get(url, headers=headers)

    def delete_media_file_request(self, device_id, request_id):
        url = '{}/v1/devices/{}/media_files/requests/{}'.format(
            BASE_URL, device_id, request_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        return requests.delete(url, headers=headers)

    def download_media_file(self, device_id, request_id, media_file_name):
        url = '{}/v1/devices/{}/media_files/requests/{}/{}'.format(
            BASE_URL, device_id, request_id, media_file_name)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        return requests.get(url, headers=headers)
