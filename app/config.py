import os 
from dotenv import load_dotenv

load_dotenv('.env')

#system
IS_LOCAL = os.environ.get("IS_LOCAL")
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

#db 
DB_TYPE = "service_account"
DB_PROJECT_ID = os.environ.get("DB_PROJECT_ID")
DB_PRIVATE_KEY_ID = os.environ.get("DB_PRIVATE_KEY_ID")
DB_PRIVATE_KEY = os.environ.get("DB_PRIVATE_KEY").replace('\\n', '\n')
DB_CLIENT_EMAIL = os.environ.get("DB_CLIENT_EMAIL")
DB_CLIENT_ID = os.environ.get("DB_CLIENT_ID")
DB_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
DB_TOKEN_URI = "https://oauth2.googleapis.com/token"
DB_AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
DB_CLIENT_X509_CERT_URL = os.environ.get("DB_CLIENT_X509_CERT_URL")