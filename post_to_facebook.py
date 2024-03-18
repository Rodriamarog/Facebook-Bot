from dotenv import load_dotenv
from scrape_wait_times import scrape_wait_times
import os
import facebook

# Load environment variables from .env file
load_dotenv()

def post_to_facebook_page_sdk(message):
    # Access variables
    access_token = os.getenv('ACCESS_TOKEN')
    page_id = os.getenv('PAGE_ID')
    graph = facebook.GraphAPI(access_token)
    
    post_id = graph.put_object(parent_object=page_id, connection_name='feed', message=message)
    
    if post_id:
        print("Successfully posted to Facebook Page.")
        return post_id
    else:
        print("Failed to post to Facebook Page.")

# Example usage
if __name__ == '__main__':
    wait_times = scrape_wait_times()
    for wait_time in wait_times:
        message = "\n".join(wait_time)
        result = post_to_facebook_page_sdk(message)
        print(result)