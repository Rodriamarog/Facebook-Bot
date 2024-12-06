import requests
import time

def download_html():
    url = "https://www.garitacenter.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Create filename with timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"border_wait_times_{timestamp}.html"
        
        # Save the HTML content
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"HTML file saved as: {filename}")
        
        # Also print the first 500 characters to check content
        print("\nFirst 500 characters of response:")
        print(response.text[:500])
        
        # Print response headers for debugging
        print("\nResponse Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    download_html()