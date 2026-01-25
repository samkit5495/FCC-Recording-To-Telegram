# FCC Recording Upload to Telegram

Automatically downloads FreeConferenceCall.com recordings and uploads them to Telegram.

## Features

- 📥 **Automatic Recording Download** - Downloads recordings from FCC
- 📤 **Telegram Upload** - Uploads to your specified Telegram group via bot
- 🔄 **Smart Credential Management** - Automatically detects expired credentials and renews them
- 🔔 **Telegram Notifications** - Real-time status updates via Telegram bot
- 🤖 **Bot-Based** - Uses Telegram Bot API (no personal account needed)
- 🐧 **Cross-Platform** - Works on Linux servers and macOS

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with the following:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_from_BotFather
TELEGRAM_CHAT_ID=your_group_chat_id

# FCC API Credentials
client_id=your_fcc_client_id
client_secret=your_fcc_client_secret
username=your_email@example.com
password=your_fcc_password

# FCC Form Fields (for automated renewal)
FCC_NAME=Your Full Name
FCC_PHONE=+1-234-567-8900
FCC_PURPOSE=Automated conference recording management and integration with Telegram bot

# Email Configuration (for credential retrieval)
EMAIL_PASSWORD=your_gmail_app_password
IMAP_SERVER=imap.gmail.com
```

**Getting Telegram Bot Credentials:**

1. **Create a bot:**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow the instructions
   - Copy the bot token (looks like `1888701686:AAHkOFo9lxv_xaDyZDsnTcEXPODYwKLaniQ`)

2. **Get Chat ID:**
   - Add your bot to the target group
   - Send a message in the group
   - Run: `python test_telegram.py --get-chat-id`
   - Copy the chat ID (negative number like `-1003590283482`)

3. **Test the connection:**
   ```bash
   python test_telegram.py
   ```

**Note:** For Gmail, create an [App Password](https://myaccount.google.com/apppasswords) instead of using your regular password.

## Usage

### Download Recordings

```bash
python3 main.py
```

The script will:
1. Connect to FCC API with stored credentials
2. If credentials are expired, automatically renew them
3. Download all available recordings
4. Upload to Telegram
5. Delete processed recordings from FCC

### Schedule Automatic Downloads

Add to crontab (run daily at 6 PM):

```bash
crontab -e
```

Add this line:

```
0 18 * * * cd /path/to/FCC_Telegram_python && ./run.sh
```

### 3. Get FCC API Credentials

**Initial Setup:**

- Visit https://www.freeconferencecall.com/for-developers/free-api
- Fill the form and get credentials via email
- Add to `.env` file

**Automatic Renewal:**

FCC credentials expire every 7 days. The script automatically detects expired credentials and renews them:
- When authentication fails, it triggers the renewal process
- Submits the form on FCC website
- Retrieves new credentials from email
- Updates `.env` file automatically
- Retries the download job with fresh credentials

No manual intervention needed! Just ensure your email credentials are configured correctly.

**Note:** For Gmail, create an [App Password](https://myaccount.google.com/apppasswords) instead of using your regular password.

## Files

- `main.py` - Main script to download and upload recordings
- `FCC.py` - FCC API wrapper class with automatic credential renewal
- `telegram_utils.py` - Telegram Bot API helper functions
- `renew_credentials.py` - Credential renewal automation (called automatically by FCC.py)
- `test_telegram.py` - Test Telegram bot connection and get chat ID
- `run.sh` - Run main script with virtual environment
- `requirements.txt` - Python package dependencies

## Telegram Notifications

The bot sends real-time updates:

**Recording Downloads:**
- 🚀 Job start notification
- 📼 Audio files uploaded directly to group
- ❌ Error notifications with full traceback
- ✅ Job completion notification

**Automatic Credential Renewal (when triggered):**
- 🔄 Invalid credentials detected
- 🚀 Renewal process started
- ✅ Form submission success
- 📧 Email checking status
- ✅ Credentials updated
- 🎉 Download job retried with new credentials

## Troubleshooting

### Telegram Bot Issues

**Test your bot connection:**

```bash
python test_telegram.py
```

**Common issues:**

- Bot not in group: Add the bot to your target group
- Wrong chat ID: Run `python test_telegram.py --get-chat-id` to find it
- Bot can't send messages: Check bot permissions in group settings
- Invalid token: Verify `TELEGRAM_BOT_TOKEN` is correct

### ChromeDriver Issues

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install chromium-browser chromium-chromedriver
pip install --upgrade selenium webdriver-manager
```

**macOS:**

```bash
brew install --cask chromedriver
```

### Email Authentication

- Use Gmail App Password, not regular password
- Enable IMAP access in Gmail settings

## How It Works

**Smart Credential Management:**

The FCC class automatically handles credential expiration:
1. Attempts authentication with stored credentials
2. Detects `invalid_client` error responses
3. Triggers automatic renewal process via Selenium
4. Retrieves new credentials from email
5. Updates `.env` file with fresh credentials
6. Retries authentication seamlessly

All happens transparently - no manual intervention needed!

## License

MIT
