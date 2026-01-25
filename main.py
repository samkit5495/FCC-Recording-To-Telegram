import requests
import traceback
import html
from datetime import datetime
from dotenv import dotenv_values
from FCC import FCC
from telegram_utils import send_telegram_message, send_telegram_file

config = dotenv_values(".env")

client_id = config['client_id']
client_secret = config['client_secret']
username = config['username']
password = config['password']

send_telegram_message('🚀 <b>Download Job Started</b>')

try:
    fcc = FCC(client_id, client_secret, username, password)
    conf = fcc.getConferences()
    for c in conf:
        print(c['id'])
        if not c['deleted'] and 'recording_url' in c and c['recording_url'] != '':
            try:
                r = requests.get(c['recording_url']+'.mp3', allow_redirects=True, verify=False)
                print('file downloaded')
                filename = datetime.fromtimestamp(c['start_time']).strftime('%Y-%m-%d')+'.mp3'
                send_telegram_file(r.content, filename)
                print('sent to telegram')
            except Exception as e:
                print(e)
                tb = html.escape(traceback.format_exc())
                send_telegram_message(f'❌ <b>Download Failed for {c["id"]}:</b>\n<pre>{tb}</pre>')
                continue
            
            # Delete conference only if download and send were successful
            try:
                fcc.deleteConference(c['id'])
                print(f'deleted conference {c["id"]}')
            except Exception as e:
                print(f'Failed to delete conference: {e}')
                tb = html.escape(traceback.format_exc())
                send_telegram_message(f'⚠️ <b>Failed to delete conference {c["id"]}:</b>\n<pre>{tb}</pre>')

    send_telegram_message('✅ <b>Download Job Completed</b>')
except Exception as e:
    tb = html.escape(traceback.format_exc())
    error_msg = f'❌ <b>Critical Job Failure:</b>\n<pre>{tb}</pre>'
    print(error_msg)
    send_telegram_message(error_msg)
