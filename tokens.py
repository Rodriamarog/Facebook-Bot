import requests
import os
from dotenv import load_dotenv

def get_permanent_page_token(app_id, app_secret, short_lived_token, page_id):
    """
    Convert a short-lived token into a permanent page token
    """
    
    # Step 1: Convert short-lived token to long-lived token
    url = f"https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_lived_token
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        long_lived_token = response.json()['access_token']
        print("Successfully got long-lived token")
        
        # Step 2: Get permanent page token
        url = f"https://graph.facebook.com/v18.0/{page_id}"
        params = {
            "fields": "access_token",
            "access_token": long_lived_token
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        permanent_token = response.json()['access_token']
        print("Successfully got permanent page token")
        
        return permanent_token
        
    except requests.exceptions.RequestException as e:
        print(f"Error getting permanent token: {e}")
        return None

def main():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    app_id = os.getenv('APP_ID')
    app_secret = os.getenv('APP_SECRET')
    page_id = os.getenv('PAGE_ID')
    short_lived_token = os.getenv('SHORT_LIVED_TOKEN')  # Get this from Graph API Explorer
    
    if not all([app_id, app_secret, page_id, short_lived_token]):
        print("Missing required environment variables")
        return
    
    permanent_token = get_permanent_page_token(app_id, app_secret, short_lived_token, page_id)
    
    if permanent_token:
        print("\nYour permanent page access token is:")
        print(permanent_token)
        print("\nStore this token in your .env file as ACCESS_TOKEN")
        
        # Optionally, automatically update the .env file
        with open('.env', 'r') as file:
            lines = file.readlines()
        
        with open('.env', 'w') as file:
            for line in lines:
                if line.startswith('ACCESS_TOKEN='):
                    file.write(f'ACCESS_TOKEN={permanent_token}\n')
                else:
                    file.write(line)
        print("\nUpdated .env file with new permanent token")

if __name__ == "__main__":
    main()