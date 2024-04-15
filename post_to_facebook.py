from dotenv import load_dotenv
from create_image_with_text import create_image_with_text
from scrape_wait_times import scrape_wait_times
import os
import facebook

# Load environment variables from .env file
load_dotenv()

def post_image_to_facebook_page(image_path):
    # Access variables
    access_token = os.getenv('ACCESS_TOKEN')
    page_id = os.getenv('PAGE_ID')
    graph = facebook.GraphAPI(access_token)
    
    # Post image to Facebook Page
    wait_times = scrape_wait_times()
    count = 1
    for wait_time in wait_times:
        text_to_print = '\n'.join(wait_time)
        create_image_with_text(text_to_print, f'wait_times{count}.png')
        count += 1
    album_path = f"{page_id}/photos"
    post_id = graph.put_photo(image=open(image_path, 'rb'), album_path=album_path)

    if post_id:
        print("Successfully posted image to Facebook Page.")
        return post_id
    else:
        print("Failed to post image to Facebook Page.")

# Example usage
if __name__ == '__main__':
    image_paths = ['wait_times1.png', 'wait_times2.png']
    for image_path in image_paths:
        result = post_image_to_facebook_page(image_path)
        print(result)
