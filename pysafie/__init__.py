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
        if res.status_code == 200:
            d = res.json()
            self.access_token = d['access_token']
            self.refresh_token = d['refresh_token']
            self.expires_at = int(time.time()) + d['expires_in']
            return True, res
        else:
            return False, res

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

    # Device APIs
    def get_device_image(self, device_id, timestamp=None):
        url = '{}/v1/devices/{}/image'.format(
            BASE_URL, device_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        if timestamp == None:
            return requests.get(url, headers=headers)
        else:
            payload = {
                'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%S+0900')
            }
            return requests.get(url, headers=headers, params=payload)

    def get_device_thumbnail(self, device_id):
        url = '{}/v1/devices/{}/thumbnail'.format(
            BASE_URL, device_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        return requests.get(url, headers=headers)

    def get_device_list(self, offset=0, limit=20, item_id=None):
        url = '{}/v1/devices'.format(BASE_URL)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        payload = {
            'offset': offset,
            'limit': limit,
            'item_id': item_id
        }
        return requests.get(url, headers=headers, params=payload)

    def register_device_event(self, device_id, event_id, timestamp):
        url = '{}/v1/devices/{}/events/{}'.format(
            BASE_URL, device_id, event_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        payload = {
            'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%S+0900')
        }
        return requests.get(url, headers=headers, params=payload)

    def get_device_event_list(self, device_id, start_datetime, end_datetime, offset=0, limit=20):
        start = start_datetime.strftime('%Y-%m-%dT%H:%M:%S+0900')
        end = end_datetime.strftime('%Y-%m-%dT%H:%M:%S+0900')
        url = '{}/v1/devices/{}/events'.format(BASE_URL, device_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        payload = {
            'start': start,
            'end': end,
            'offset': offset,
            'limit': limit
        }
        return requests.get(url, headers=headers, params=payload)

    def get_device_media_list(self, device_id, start_datetime, end_datetime):
        start = start_datetime.strftime('%Y-%m-%dT%H:%M:%S+0900')
        end = end_datetime.strftime('%Y-%m-%dT%H:%M:%S+0900')
        url = '{}/v1/devices/{}/media'.format(BASE_URL, device_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        payload = {
            'start': start,
            'end': end
        }
        return requests.get(url, headers=headers, params=payload)

    def get_device_location(self, device_id):
        url = '{}/v1/devices/{}/location'.format(BASE_URL, device_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        return requests.get(url, headers=headers)

    def get_device_still_capture(self, device_id):
        url = '{}/v1/devices/{}/still_capture'.format(BASE_URL, device_id)
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        return requests.post(url, headers=headers)

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
        return requests.post(url, headers=headers, data=json.dumps(payload))

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
