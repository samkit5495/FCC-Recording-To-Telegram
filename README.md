# FCC Recording Upload to Telegram

Automatically downloads FreeConferenceCall.com recordings and uploads them to Telegram.

## Features

- 📥 **Automatic Recording Download** - Downloads recordings from FCC
- 📤 **Telegram Upload** - Uploads to your specified Telegram group via bot
- 🔄 **Auto Credential Renewal** - Automatically renews FCC API credentials every 7 days
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

### 3. Get FCC API Credentials

**Option 1: Manual (first time)**

- Visit https://www.freeconferencecall.com/for-developers/free-api
- Fill the form and get credentials via email
- Add to `.env` file

**Option 2: Automated (recommended)**

- See [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) for automated renewal setup
- Credentials will be automatically renewed every 7 days

## Usage

### Download Recordings Manually

```bash
python3 main.py
```

### Schedule Automatic Downloads

Add to crontab (run daily at 6 PM):

```bash
crontab -e
```

Add this line:

```
0 18 * * * cd /path/to/FCC_Telegram_python && ./run.sh
```

### Automated Credential Renewal

FCC credentials expire every 7 days. Automate renewal with:

#### Cron Job

Edit crontab:

```bash
crontab -e
```

Add this line (runs every 6 days at 2 AM):

```
0 2 */6 * * cd /path/to/FCC_Telegram_python && ./renew.sh >> /path/to/FCC_Telegram_python/cron_renewal.log 2>&1
```

### Test Credential Renewal

```bash
./renew.sh
```

## Files

- `main.py` - Main script to download and upload recordings
- `FCC.py` - FCC API wrapper class
- `renew_credentials.py` - Automated credential renewal script
- `test_telegram.py` - Test Telegram bot connection and get chat ID
- `run.sh` - Run main script with virtual environment
- `renew.sh` - Run credential renewal with virtual environment
- `AUTOMATION_SETUP.md` - Detailed automation setup guide

## Telegram Notifications

The bot sends real-time updates for both recording downloads and credential renewal:

**Recording Downloads:**
- 🚀 Job start notification
- 📼 Audio files uploaded directly to group
- ❌ Error notifications if download fails
- ✅ Job completion notification

**Credential Renewal:**
- 🚀 Process start
- ✅ Form submission success
- 📧 Email checking status
- ✅ Credentials received
- 🎉 Process completion
- ❌ Any errors

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

## Documentation

- [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) - Complete automation setup guide
- Includes Linux server deployment instructions
- Cross-platform support (macOS for testing, Linux for production)

## License

MIT
