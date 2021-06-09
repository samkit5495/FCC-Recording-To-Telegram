import requests
import urllib

class FCC:

    base_url = 'https://www.freeconferencecall.com/api/'

    def call(self, req_type, url, data={}):
        if req_type =='post':
            return requests.post(self.base_url+url,data=data, headers={
                'Authorization':'Bearer '+self.access_token
            }).json()
        elif req_type=='get':
            return requests.get(self.base_url+url+'?'+urllib.parse.urlencode(data), headers={
                'Authorization':'Bearer '+self.access_token
            }).json()
        elif req_type=='delete':
            return requests.delete(self.base_url+url, headers={
                'Authorization':'Bearer '+self.access_token
            }).json()

    def __init__(self, client_id, client_secret, username, password):
        resp = requests.post(self.base_url+'v4/token',{
            'grant_type':'password',
            'client_id':client_id,
            'client_secret':client_secret,
            'username':username,
            'password':password
        }).json()
        print(resp)
        self.access_token = resp['access_token']

    def getConferences(self):
        resp = self.call('get', 'v4/conferences', {
            'has_recordings':'true',
            'order_by':'start_date',
            'order':'DESC'
        })
        return resp['conferences']
    
    def deleteConference(self, id):
        resp = self.call('delete', 'v4/conferences/{0}'.format(id))
        return resp
