import requests
import urllib
from datetime import datetime
from dotenv import dotenv_values
from FCC import FCC

config = dotenv_values(".env")

# Telegram Bot Configuration
bot_token = config['TELEGRAM_BOT_TOKEN']
chat_id = config['TELEGRAM_CHAT_ID']

def send_telegram_message(message):
    """Send message using Telegram Bot API"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send Telegram message: {str(e)}")
        return False

def send_telegram_file(file_content, filename):
    """Send audio file using Telegram Bot API"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
        files = {
            'audio': (filename, file_content, 'audio/mpeg')
        }
        data = {
            'chat_id': chat_id,
            'caption': f'📼 Recording: {filename}'
        }
        response = requests.post(url, files=files, data=data, timeout=60)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send Telegram file: {str(e)}")
        return False

client_id = config['client_id']
client_secret = config['client_secret']
username = config['username']
password = config['password']

send_telegram_message('🚀 <b>Download Job Started</b>')

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
            send_telegram_message(f'❌ <b>Download Job Failed:</b> {str(e)}')
        else:
            fcc.deleteConference(c['id'])

send_telegram_message('✅ <b>Download Job Completed</b>')
