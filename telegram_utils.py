import requests
from dotenv import dotenv_values

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
        if response.status_code != 200:
            print(f"Telegram API error: {response.status_code} - {response.text}")
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
