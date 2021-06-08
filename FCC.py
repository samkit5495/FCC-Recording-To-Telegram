import requests
import urllib
from datetime import datetime
from telethon import TelegramClient, events, sync
from dotenv import dotenv_values
config = dotenv_values(".env") 

api_id = config['api_id']
api_hash = config['api_hash']
client = TelegramClient('session_name', api_id, api_hash).start()

for dialog in client.iter_dialogs():
    if dialog.name == config['sendTo']:
        my_private_channel = dialog
        break

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
            'order':'ASC'
        })
        return resp['conferences']
    
    def deleteConference(self, id):
        resp = self.call('delete', 'v4/conferences/{0}'.format(id))
        return resp

client_id = config['client_id']
client_secret = config['client_secret']
username = config['username']
password = config['password']

fcc = FCC(client_id, client_secret, username, password)
conf = fcc.getConferences()
for c in conf:
    print(c['id'])
    if not c['deleted'] and 'recording_url' in c and c['recording_url']!='':
        try:
            r = requests.get(c['recording_url']+'.mp3', allow_redirects=True)
            print('file downloaded')
            file = client.upload_file(r.content, file_name=datetime.fromtimestamp(c['start_time']).strftime('%Y-%m-%d')+'.mp3')
            message = client.send_file(my_private_channel, file)
            print('sent to telegram')
        except Exception as e:
            print(e)
        else:
            fcc.deleteConference(c['id'])



