"""
Automated FCC Credentials Renewal Script
Automates the process of requesting new FCC API credentials every 7 days
"""

import os
import re
import time
import imaplib
import email
from email.header import decode_header
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import dotenv_values, set_key
from telethon import TelegramClient
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('credential_renewal.log'),
        logging.StreamHandler()
    ]
)

class FCCCredentialRenewer:
    def __init__(self):
        self.env_file = '.env'
        self.config = dotenv_values(self.env_file)
        self.fcc_url = "https://www.freeconferencecall.com/for-developers/free-api?country_code=in&locale=global"
        
        # Get form data from config or set defaults
        self.form_data = {
            'name': self.config.get('FCC_NAME', 'Your Name'),
            'email': self.config.get('username'),
            'phone': self.config.get('FCC_PHONE', ''),
            'purpose': self.config.get('FCC_PURPOSE', 'Automated conference recording management and integration with Telegram bot')
        }
        
        # Initialize Telegram client if credentials available
        self.telegram_client = None
        self.telegram_channel = None
        if self.config.get('api_id') and self.config.get('api_hash'):
            try:
                self.telegram_client = TelegramClient('renewal_session', 
                                                     self.config['api_id'], 
                                                     self.config['api_hash'])
                self.telegram_client.start()
                
                # Find the target channel/chat
                for dialog in self.telegram_client.iter_dialogs():
                    if dialog.name == self.config.get('sendTo'):
                        self.telegram_channel = dialog
                        break
                        
                logging.info("✓ Telegram client initialized")
            except Exception as e:
                logging.warning(f"Could not initialize Telegram: {str(e)}")
                self.telegram_client = None
    
    def send_telegram_message(self, message):
        """Send status update to Telegram"""
        try:
            if self.telegram_client and self.telegram_channel:
                self.telegram_client.send_message(self.telegram_channel, message)
                logging.info(f"Telegram notification sent: {message[:50]}...")
        except Exception as e:
            logging.warning(f"Failed to send Telegram message: {str(e)}")
        
    def request_new_credentials(self):
        """Automate form submission on FCC website"""
        logging.info("Starting credential request process...")
        self.send_telegram_message("🔄 FCC Credential Renewal: Starting form submission...")
        
        # Setup Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')  # Use new headless mode
        chrome_options.add_argument('--no-sandbox')  # Required for Linux
        chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems on Linux
        chrome_options.add_argument('--disable-gpu')  # Applicable to Linux
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Avoid detection
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        driver = None
        try:
            # Try to initialize ChromeDriver (works on both Linux and Mac)
            # Selenium 4.6+ has built-in driver management
            try:
                # Try using Selenium's built-in manager first (most reliable)
                driver = webdriver.Chrome(options=chrome_options)
                logging.info("ChromeDriver initialized using Selenium Manager")
            except Exception as e1:
                logging.warning(f"Selenium Manager failed: {str(e1)}")
                try:
                    # Fallback to webdriver-manager
                    from selenium.webdriver.chrome.service import Service
                    from webdriver_manager.chrome import ChromeDriverManager
                    
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    logging.info("ChromeDriver initialized using webdriver-manager")
                except Exception as e2:
                    logging.error(f"webdriver-manager also failed: {str(e2)}")
                    raise Exception("Could not initialize ChromeDriver. Please install Chrome and ChromeDriver manually.")
            
            driver.get(self.fcc_url)
            
            # Wait for page to load
            wait = WebDriverWait(driver, 20)
            
            logging.info("Waiting for form to load...")
            time.sleep(3)  # Wait for page to fully load
            
            # Find and fill all form fields
            logging.info("Filling form fields...")
            
            try:
                # Fill Name field
                name_field = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@placeholder='Name' or @name='name' or contains(@id, 'name')]")))
                name_field.clear()
                name_field.send_keys(self.form_data['name'])
                logging.info(f"✓ Filled name: {self.form_data['name']}")
                time.sleep(0.5)
                
                # Fill Email field
                email_field = driver.find_element(
                    By.XPATH, "//input[@placeholder='Email' or @name='email' or @type='email']")
                email_field.clear()
                email_field.send_keys(self.form_data['email'])
                logging.info(f"✓ Filled email: {self.form_data['email']}")
                time.sleep(0.5)
                
                # Fill Phone field
                phone_field = driver.find_element(
                    By.XPATH, "//input[@placeholder='Phone' or @name='phone' or contains(@id, 'phone') or @type='tel']")
                phone_field.clear()
                phone_field.send_keys(self.form_data['phone'])
                logging.info(f"✓ Filled phone: {self.form_data['phone']}")
                time.sleep(0.5)
                
                # Fill Purpose/Integration field (could be textarea or input)
                purpose_field = driver.find_element(
                    By.XPATH, "//textarea[@placeholder='Please explain what you are trying to achieve with this integration' or contains(@placeholder, 'integration')] | //input[contains(@placeholder, 'integration')]")
                purpose_field.clear()
                purpose_field.send_keys(self.form_data['purpose'])
                logging.info(f"✓ Filled purpose: {self.form_data['purpose'][:50]}...")
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"Error finding form fields: {str(e)}")
                logging.info("Trying alternative selectors...")
                
                # Fallback: Try to find all input fields and fill them in order
                inputs = driver.find_elements(By.TAG_NAME, "input")
                textareas = driver.find_elements(By.TAG_NAME, "textarea")
                
                form_values = [self.form_data['name'], self.form_data['email'], self.form_data['phone']]
                for i, input_field in enumerate(inputs[:3]):
                    if input_field.is_displayed() and i < len(form_values):
                        input_field.clear()
                        input_field.send_keys(form_values[i])
                        time.sleep(0.5)
                
                if textareas:
                    textareas[0].clear()
                    textareas[0].send_keys(self.form_data['purpose'])
                    time.sleep(0.5)
            
            # Submit the form
            logging.info("Submitting form...")
            submit_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Request Access')] | //button[@type='submit'] | //input[@type='submit']")
            ))
            submit_button.click()
            
            logging.info("Form submitted successfully!")
            self.send_telegram_message("✅ FCC Form submitted successfully! Waiting for credentials email...")
            time.sleep(5)  # Wait for submission
            
            return True
            
        except Exception as e:
            logging.error(f"Error during form submission: {str(e)}")
            self.send_telegram_message(f"❌ FCC Form submission failed: {str(e)}")
            return False
        finally:
            if driver:
                driver.quit()
    
    def check_email_for_credentials(self, max_wait_minutes=10):
        """Check email for FCC credentials"""
        logging.info("Checking email for new credentials...")
        self.send_telegram_message("📧 Checking email for FCC credentials...")
        
        # Email configuration - add these to .env file
        imap_server = self.config.get('IMAP_SERVER', 'imap.gmail.com')
        email_address = self.config['username']
        email_password = self.config.get('EMAIL_PASSWORD', self.config['password'])
        
        try:
            # Connect to email server
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(email_address, email_password)
            mail.select('inbox')
            
            # Search for recent FCC emails
            # Wait up to max_wait_minutes for the email to arrive
            start_time = time.time()
            credentials_found = False
            
            while (time.time() - start_time) < (max_wait_minutes * 60):
                # Search for emails from FCC
                status, messages = mail.search(None, 'FROM "freeconferencecall.com"')
                
                if status == 'OK':
                    email_ids = messages[0].split()
                    
                    # Check the most recent emails (last 5)
                    for email_id in email_ids[-5:]:
                        status, msg_data = mail.fetch(email_id, '(RFC822)')
                        
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                
                                # Get email subject
                                subject = decode_header(msg['Subject'])[0][0]
                                if isinstance(subject, bytes):
                                    subject = subject.decode()
                                
                                # Check if this is the credentials email
                                if 'api' in subject.lower() or 'credential' in subject.lower():
                                    # Extract credentials from email body
                                    credentials = self._extract_credentials_from_email(msg)
                                    
                                    if credentials:
                                        logging.info("Credentials found in email!")
                                        self.send_telegram_message("✅ Credentials received! Updating .env file...")
                                        credentials_found = True
                                        mail.close()
                                        mail.logout()
                                        return credentials
                
                if not credentials_found:
                    logging.info(f"Waiting for email... ({int(time.time() - start_time)}s)")
                    time.sleep(30)  # Check every 30 seconds
            
            mail.close()
            mail.logout()
            logging.warning("Timeout: Credentials email not received within expected time")
            return None
            
        except Exception as e:
            logging.error(f"Error checking email: {str(e)}")
            self.send_telegram_message(f"❌ Error checking email: {str(e)}")
            return None
    
    def _extract_credentials_from_email(self, msg):
        """Extract client_id and client_secret from email"""
        try:
            # Get email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
                    elif part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode()
            
            logging.info("Email body received, extracting credentials...")
            
            # Extract credentials using regex - matching FCC's actual format
            # Format: <b>Public API key:</b> 99e78c7d09c8ca55 <br>
            # Format: <b>Private API key:</b> 4393e0302abdb06cd5d0cb932fbb4d83714f1bf28118e9e6 <br>
            
            public_key_match = re.search(
                r'Public\s+API\s+key[:\s]*</b>\s*([a-f0-9]+)',
                body, re.IGNORECASE
            )
            private_key_match = re.search(
                r'Private\s+API\s+key[:\s]*</b>\s*([a-f0-9]+)',
                body, re.IGNORECASE
            )
            
            # Fallback patterns for plain text or other formats
            if not public_key_match:
                public_key_match = re.search(
                    r'(?:Public\s+API\s+key|client[_\s]*id)[:\s]*([a-f0-9]+)',
                    body, re.IGNORECASE
                )
            
            if not private_key_match:
                private_key_match = re.search(
                    r'(?:Private\s+API\s+key|client[_\s]*secret)[:\s]*([a-f0-9]+)',
                    body, re.IGNORECASE
                )
            
            if public_key_match and private_key_match:
                credentials = {
                    'client_id': public_key_match.group(1),
                    'client_secret': private_key_match.group(1)
                }
                logging.info(f"✓ Extracted client_id: {credentials['client_id']}")
                logging.info(f"✓ Extracted client_secret: {credentials['client_secret'][:10]}...")
                return credentials
            else:
                logging.error("Could not find credentials in email body")
                logging.debug(f"Email body snippet: {body[:500]}")
            
        except Exception as e:
            logging.error(f"Error extracting credentials: {str(e)}")
        
        return None
    
    def update_env_file(self, credentials):
        """Update .env file with new credentials"""
        try:
            env_path = os.path.abspath(self.env_file)
            
            set_key(env_path, 'client_id', credentials['client_id'])
            set_key(env_path, 'client_secret', credentials['client_secret'])
            
            logging.info("✓ .env file updated successfully!")
            logging.info(f"New client_id: {credentials['client_id']}")
            logging.info(f"New client_secret: {credentials['client_secret'][:10]}...")
            
            self.send_telegram_message(f"✅ .env updated!\nNew client_id: {credentials['client_id']}\nExpires in ~7 days")
            
            return True
        except Exception as e:
            logging.error(f"Error updating .env file: {str(e)}")
            return False
    
    def renew_credentials(self):
        """Main method to renew credentials"""
        logging.info("=" * 50)
        logging.info("Starting FCC Credential Renewal Process")
        logging.info("=" * 50)
        
        self.send_telegram_message("🚀 FCC Credential Renewal Process Started")
        
        # Step 1: Request new credentials
        # if not self.request_new_credentials():
        #     logging.error("Failed to request credentials. Aborting.")
        #     return False
        
        # Step 2: Check email for credentials
        credentials = self.check_email_for_credentials()
        
        if not credentials:
            logging.error("Failed to retrieve credentials from email. Aborting.")
            return False
        
        # Step 3: Update .env file
        if not self.update_env_file(credentials):
            logging.error("Failed to update .env file. Aborting.")
            return False
        
        logging.info("=" * 50)
        logging.info("Credential renewal completed successfully!")
        logging.info("=" * 50)
        
        self.send_telegram_message("🎉 FCC Credential Renewal Completed Successfully!")
        
        # Cleanup Telegram client
        if self.telegram_client:
            self.telegram_client.disconnect()
        
        return True


def main():
    """Run the credential renewal process"""
    renewer = FCCCredentialRenewer()
    success = renewer.renew_credentials()
    
    if success:
        print("\n✓ Credentials renewed successfully!")
    else:
        print("\n✗ Credential renewal failed. Check logs for details.")
    
    return success


if __name__ == "__main__":
    main()
