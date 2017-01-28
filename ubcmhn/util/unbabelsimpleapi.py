import requests
import os
import json

UNBABEL_SANDBOX_API_URL = os.environ.get('UNBABEL_SANDOX_API_URL',
                                         "http://sandbox.unbabel.com/tapi/v2/")
UNBABEL_API_URL = os.environ.get('UNBABEL_API_URL',
                                 "https://unbabel.com/tapi/v2/")

class UnbabelSimpleApi(object):
    def __init__(self, username, api_key, sandbox=False):
        if sandbox:
            api_url = UNBABEL_SANDBOX_API_URL
        else:
            api_url = UNBABEL_API_URL
        self.username = username
        self.api_key = api_key
        self.api_url = api_url
        self.is_bulk = False
        self.headers = {
            'Authorization': 'ApiKey {}:{}'.format(self.username, self.api_key),
            'content-type': 'application/json'}


    def post_translation(self, text, source_language, target_language):

        data = {
            "text" : text,
            "source_language" : source_language,
            "target_language" : target_language
        }

        result = requests.post("%stranslation/" % self.api_url, headers=self.headers, data=json.dumps(data))
        if result.status_code in (201, 202):
            json_object = json.loads(result.content.decode('utf-8-sig'))
            return json_object
        elif result.status_code == 401:
            raise Exception(result.content)
        elif result.status_code == 400:
            print("text={0} srcl={1} tgtlng={2}".format(text, source_language, target_language))
            raise Exception(result.content)
        else:
            raise Exception("Unknown Error return status %d: %s", result.status_code, result.content[0:100])


    def api_call(self, uri, data=None, internal_api_call=False):
        api_url = self.api_url
        if internal_api_call:
            api_url = api_url.replace('/tapi/v2/', '/api/v1/')
        url = "{}{}".format(api_url, uri)
        if data is None:
            return requests.get(url, headers=self.headers)
        return requests.post(url, headers=self.headers, data=json.dumps(data))


    def get_translation(self, uid):
        '''
            Returns a translation with the given id
        '''
        result = self.api_call('translation/{}/'.format(uid))
        if result.status_code == 200:
            return json.loads(result.content.decode('utf-8'))
        else:
            raise ValueError(result.content)

    def __repr__(self):
        return "<UnbabelSimpleApi un({0}) ak({1})>".format(self.username, self.api_key)
