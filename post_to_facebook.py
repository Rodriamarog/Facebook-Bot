from dotenv import load_dotenv
from create_image_with_text import create_image_with_text
from scrape_wait_times import scrape_wait_times
import os
import facebook
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def post_to_facebook_page(image_path, wait_time_data):
    # Access variables
    access_token = os.getenv('ACCESS_TOKEN')
    page_id = os.getenv('PAGE_ID')
    graph = facebook.GraphAPI(access_token)

    # Determine the border crossing point from the image filename
    if "1" in image_path:
        crossing_point = "San Ysidro"
        place_id = '115318908567372'  # San Ysidro Border Crossing Place ID
    else:
        crossing_point = "Otay"
        place_id = '172775682873255'  # Otay Border Crossing Place ID

    # Get current time
    current_time = datetime.now().strftime("%H:%M")

    # Create message
    message = f"Asi esta la linea en {crossing_point} a las {current_time}\n\n"
    if crossing_point == "San Ysidro":
        message += "#sanysidro #tijuana #garita #comoestalalinea #sentri #readylane"
    else:
        message += "#otay #tijuana #garita #comoestalalinea #sentri #readylane"

    # Post image with message and location to Facebook Page
    with open(image_path, 'rb') as image_file:
        post_id = graph.put_photo(
            image=image_file,
            message=message,
            album_path=f"{page_id}/photos",
            place=place_id
        )

    if post_id:
        print(f"Successfully posted image for {crossing_point} to Facebook Page.")
        return post_id
    else:
        print(f"Failed to post image for {crossing_point} to Facebook Page.")

# Main execution
if __name__ == '__main__':
    wait_times = scrape_wait_times()
    count = 1
    for wait_time in wait_times:
        text_to_print = '\n'.join(wait_time)
        image_path = f'wait_times{count}.png'
        create_image_with_text(text_to_print, image_path)
        result = post_to_facebook_page(image_path, wait_time)
        print(result)
        count += 1