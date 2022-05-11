import requests
import urllib
from datetime import datetime
from telethon import TelegramClient, events, sync
from dotenv import dotenv_values
from FCC import FCC

config = dotenv_values(".env")

api_id = config['api_id']
api_hash = config['api_hash']
client = TelegramClient('session_name', api_id, api_hash).start()

for dialog in client.iter_dialogs():
    if dialog.name == config['sendTo']:
        my_private_channel = dialog
        break

client_id = config['client_id']
client_secret = config['client_secret']
username = config['username']
password = config['password']

client.send_message(my_private_channel, 'Download Job Started')

fcc = FCC(client_id, client_secret, username, password)
conf = fcc.getConferences()
for c in conf:
    print(c['id'])
    if not c['deleted'] and 'recording_url' in c and c['recording_url'] != '':
        try:
            r = requests.get(c['recording_url']+'.mp3', allow_redirects=True)
            print('file downloaded')
            file = client.upload_file(r.content, file_name=datetime.fromtimestamp(c['start_time']).strftime('%Y-%m-%d')+'.mp3')
            message = client.send_file(my_private_channel, file)
            print('sent to telegram')
        except Exception as e:
            print(e)
            client.send_message(my_private_channel, 'Download Job Failed: '+str(e))
        else:
            fcc.deleteConference(c['id'])

client.send_message(my_private_channel, 'Download Job Completed')
