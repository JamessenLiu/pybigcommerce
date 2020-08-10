import requests


class Connection:

    def __init__(self, store_hash, access_token):
        self.endpoint = 'https://api.bigcommerce.com/stores'
        self.session = requests.session()
        self.store_hash = store_hash
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Auth-Client": access_token,
            "X-Auth-Token": access_token
        }

    def get_method(self, uri, params=None, version='v2'):
        url = "{0}/{1}/{2}".format(self.endpoint, self.store_hash, version) + uri
        resp = self.session.get(url, headers=self.headers, params=params)
        if resp.status_code == 200:
            result = resp.json()
        else:
            result = False
        return result

    def delete_method(self, uri, params=None, version='v2'):
        url = "{0}/{1}/{2}".format(self.endpoint, self.store_hash, version) + uri
        resp = self.session.delete(
            url, headers=self.headers, params=params)
        if resp.status_code == 200:
            result = resp.json()
        else:
            result = False
        return result

    def post_method(self, uri, data, version='v2'):

        url = "{0}/{1}/{2}".format(self.endpoint, self.store_hash, version) + uri
        resp = self.session.post(
            url, headers=self.headers, data=data)
        if resp.status_code == 200 or resp.status_code == 201:
            result = resp.json()
        else:
            result = False
        return result

    def put_method(self, uri, data, version='v2'):

        url = "{0}/{1}/{2}".format(self.endpoint, self.store_hash, version) + uri
        resp = self.session.put(
            url, headers=self.headers, data=data)
        if resp.status_code == 200 or resp.status_code == 201:
            result = resp.json()
        else:
            result = False
        return result
