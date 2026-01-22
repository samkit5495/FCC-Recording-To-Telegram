# FCC Recording Upload to Telegram

Automatically downloads FreeConferenceCall.com recordings and uploads them to Telegram.

## Features

- 📥 **Automatic Recording Download** - Downloads recordings from FCC
- 📤 **Telegram Upload** - Uploads to your specified Telegram channel/chat
- 🔄 **Auto Credential Renewal** - Automatically renews FCC API credentials every 7 days
- 🔔 **Telegram Notifications** - Real-time status updates via Telegram
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
# Telegram Configuration
api_id=your_telegram_api_id
api_hash=your_telegram_api_hash
sendTo=Your Channel Name

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

#### Option 1: Cron Job (recommended for servers)

Edit crontab:

```bash
crontab -e
```

Add this line (runs every 6 days at 2 AM):

```
0 2 */6 * * cd /path/to/FCC_Telegram_python && /usr/bin/python3 renew_credentials.py >> /path/to/FCC_Telegram_python/cron_renewal.log 2>&1
```

#### Option 2: Systemd Service (Linux)

See [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) for detailed setup instructions.

### Test Credential Renewal

```bash
python3 renew_credentials.py
```

## Files

- `main.py` - Main script to download and upload recordings
- `FCC.py` - FCC API wrapper class
- `renew_credentials.py` - Automated credential renewal script
- `scheduler.py` - Scheduler for automated renewals
- `setup_cron.sh` - Setup cron job for renewals
- `AUTOMATION_SETUP.md` - Detailed automation setup guide

## Telegram Notifications

The credential renewal process sends real-time updates:

- 🚀 Process start
- ✅ Form submission success
- 📧 Email checking status
- ✅ Credentials received
- 🎉 Process completion
- ❌ Any errors

## Troubleshooting

### ChromeDriver Issues

- Script automatically manages ChromeDriver
- For manual installation: `brew install --cask chromedriver` (macOS)

### Email Authentication

- Use Gmail App Password, not regular password
- Enable IMAP access in Gmail settings

### Telegram Connection

- Ensure `api_id` and `api_hash` are correct
- Run `main.py` once to create session file

## Documentation

- [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) - Complete automation setup guide
- Includes Linux server deployment instructions
- Cross-platform support (macOS for testing, Linux for production)

## License

MIT
