import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_long_lived_token(app_id, app_secret, short_lived_token):
    url = "https://graph.facebook.com/v12.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_lived_token
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'access_token' in data:
        return data['access_token']
    else:
        return "Error: " + data.get('error', {}).get('message', '')

app_id=os.getenv('APP_ID')
app_secret=os.getenv('APP_SECRET')
access_token=os.getenv('ACCESS_TOKEN')

# Example usage
long_lived_token = get_long_lived_token(app_id, app_secret, access_token)
print(long_lived_token)
