"""
Test Telegram Bot Connection
Tests if the bot can send messages to the configured group
"""

import requests
from dotenv import dotenv_values

def test_telegram_connection():
    """Test Telegram bot connection and send a test message"""
    
    # Load configuration from .env file
    config = dotenv_values('.env')
    bot_token = config.get('TELEGRAM_BOT_TOKEN')
    chat_id = config.get('TELEGRAM_CHAT_ID')
    
    print("=" * 50)
    print("Testing Telegram Bot Connection")
    print("=" * 50)
    
    # Check if credentials are configured
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file")
        return False
    
    if not chat_id:
        print("❌ Error: TELEGRAM_CHAT_ID not found in .env file")
        return False
    
    print(f"✓ Bot Token: {bot_token[:10]}...{bot_token[-5:]}")
    print(f"✓ Chat ID: {chat_id}")
    print()
    
    # Test 1: Get bot information
    print("Test 1: Getting bot information...")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Bot connected successfully!")
                print(f"   Bot Name: {bot_info.get('first_name')}")
                print(f"   Username: @{bot_info.get('username')}")
                print(f"   Bot ID: {bot_info.get('id')}")
            else:
                print(f"❌ Failed: {data.get('description', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to bot: {str(e)}")
        return False
    
    print()
    
    # Test 2: Send test message to group
    print("Test 2: Sending test message to group...")
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': '🧪 <b>Test Message</b>\n\nThis is a test message from the FCC Credential Renewal Bot.\n\nIf you see this, the bot is configured correctly! ✅',
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print("✅ Test message sent successfully!")
                print(f"   Message ID: {data['result'].get('message_id')}")
                chat_info = data['result'].get('chat', {})
                print(f"   Chat: {chat_info.get('title', chat_info.get('first_name', 'Unknown'))}")
                print(f"   Chat Type: {chat_info.get('type')}")
            else:
                print(f"❌ Failed: {data.get('description', 'Unknown error')}")
                return False
        else:
            error_data = response.json()
            print(f"❌ HTTP Error {response.status_code}")
            print(f"   Error: {error_data.get('description', response.text)}")
            
            # Provide helpful hints for common errors
            if response.status_code == 400:
                print("\n💡 Hint: Check if your TELEGRAM_CHAT_ID is correct.")
                print("   For groups, it should start with a minus sign (e.g., -1001234567890)")
            elif response.status_code == 403:
                print("\n💡 Hint: The bot may not have permission to send messages.")
                print("   Make sure the bot is added to the group and has send message permissions.")
            
            return False
    except Exception as e:
        print(f"❌ Error sending message: {str(e)}")
        return False
    
    print()
    print("=" * 50)
    print("All tests passed! ✅")
    print("=" * 50)
    return True


def get_chat_id():
    """Helper function to get chat ID from recent messages"""
    config = dotenv_values('.env')
    bot_token = config.get('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    print("\nFetching recent updates to find chat IDs...\n")
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                updates = data.get('result', [])
                
                if not updates:
                    print("No recent messages found.")
                    print("\n💡 Send a message in your group (with the bot added) and run this again.")
                    return
                
                print("Found chat IDs:\n")
                seen_chats = set()
                
                for update in updates:
                    chat = None
                    if 'message' in update:
                        chat = update['message'].get('chat')
                    elif 'my_chat_member' in update:
                        chat = update['my_chat_member'].get('chat')
                    
                    if chat and chat['id'] not in seen_chats:
                        seen_chats.add(chat['id'])
                        print(f"Chat ID: {chat['id']}")
                        print(f"   Name: {chat.get('title', chat.get('first_name', 'Unknown'))}")
                        print(f"   Type: {chat['type']}")
                        print()
            else:
                print(f"❌ Failed: {data.get('description', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--get-chat-id":
        get_chat_id()
    else:
        success = test_telegram_connection()
        
        if not success:
            print("\n💡 To find your chat ID, run: python test_telegram.py --get-chat-id")
            sys.exit(1)
