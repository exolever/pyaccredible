import requests
import json


class AccredibleWrapper:

    PRODUCTION_API_URL = 'https://api.accredible.com/v1/'

    def __init__(self, key, server=None):
        self.key = key
        if not server:
            self.API_URL = self.PRODUCTION_API_URL
        else:
            self.API_URL = server

    def build_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Token token={}'.format(self.key)
        }

    @property
    def group_url(self):
        return '{}issuer/groups'.format(self.API_URL)

    def get(self, url, data):
        return requests.get(url, data=data, headers=self.build_headers())

    def post(self, url, data):
        return requests.post(url, data=json.dumps(data), headers=self.build_headers())

    def put(self, url, data):
        return requests.put(url, data=json.dumps(data), headers=self.build_headers())

    def delete(self, url, data):
        return requests.delete(url, headers=self.build_headers())

    def group_create(self, **kwargs):
        data = {
            'group': kwargs
        }
        url = self.group_url
        return self.post(url, data)

    def credential_create(self, group_id, name, email, issued_on, custom_attrs={}):
        data = {
            'credential': {
                'recipient': {
                    'name': name,
                    'email': email,
                },
                'group_id': group_id,
                'issued_on': issued_on.strftime("%Y-%m-%d")
            }
        }
        if custom_attrs:
            data['credential']['custom_attributes'] = custom_attrs
        url = '{}credentials'.format(self.API_URL)
        return self.post(url, data)

    def credential_update(self, credential_id, **kwargs):
        data = {
            'credential': kwargs
        }
        url = '{}credentials/{}'.format(self.API_URL, credential_id)
        return self.put(url, data)

    def credential_create_bulk(self, group_id, participants, issued_on=None, custom_attrs={}):
        data = {
            'credentials': []
        }
        for participant in participants:
            recipient = {
                'recipient': {
                    'name': participant[0],
                    'email': participant[1],
                },
                'group_id': group_id,
            }
            if issued_on:
                recipient['issued_on'] = issued_on.strftime("%Y-%m-%d")
            if custom_attrs:
                recipient['custom_attributes'] = custom_attrs
            data['credentials'].append(recipient)
        url = '{}credentials/bulk_create'.format(self.API_URL)
        return self.post(url, data)

    def generate_pdf(self, credential_id):
        data = {}
        url = '{}credentials/generate_single_pdf/{}'.format(
            self.API_URL,
            credential_id)
        return self.post(url, data)

    def generate_bulk_pdf(self, credentials_id):
        data = {
            'credentials': credentials_id,
        }
        url = '{}credentials/generate_pdf'.format(
            self.API_URL)
        return self.post(url, data)
