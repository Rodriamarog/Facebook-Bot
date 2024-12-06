import os
import facebook
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict
import logging
from create_image_with_text import create_border_image
from scrape_wait_times import get_wait_times

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def post_to_facebook_page(image_path: str, border_type: str) -> str:
    """Post border wait times image to Facebook page"""
    
    # Access credentials
    access_token = os.environ.get('ACCESS_TOKEN')
    page_id = os.environ.get('PAGE_ID')
    
    if not all([access_token, page_id]):
        logger.error("Missing required environment variables")
        return None
        
    graph = facebook.GraphAPI(access_token=access_token, version="3.0")
    
    # Set place ID based on border type
    place_ids = {
        "San Ysidro": "115318908567372",
        "Otay Mesa": "172775682873255"
    }
    
    # Create message
    current_time = datetime.now().strftime("%H:%M")
    
    hashtags = {
        "San Ysidro": "#sanysidro #tijuana #garita #comoestalalinea #sentri #readylane",
        "Otay Mesa": "#otay #tijuana #garita #comoestalalinea #sentri #readylane"
    }
    
    message = (f"Asi esta la linea en {border_type} a las {current_time}\n\n"
               f"{hashtags[border_type]}")
    
    # Post to Facebook
    try:
        with open(image_path, 'rb') as image_file:
            post_id = graph.put_photo(
                image=image_file,
                message=message,
                album_path=f"{page_id}/photos",
                place=place_ids[border_type]
            )
            
        logger.info(f"Successfully posted {border_type} image to Facebook")
        
        # Clean up image file
        try:
            os.remove(image_path)
            logger.info(f"Successfully deleted {image_path}")
        except OSError as e:
            logger.error(f"Error deleting {image_path}: {e}")
            
        return post_id.get('post_id')
        
    except facebook.GraphAPIError as e:
        logger.error(f"Facebook API Error: {e}")
        logger.error(f"Error Type: {type(e)}")
        logger.error(f"Error Args: {e.args}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error posting to Facebook: {e}")
        return None

def post_border_wait_times():
    """Main function to fetch wait times and post to Facebook"""
    
    try:
        # Get wait times from API
        wait_times = get_wait_times()
        if not wait_times:
            logger.error("Failed to fetch wait times")
            return
            
        # Create and post images for each border
        borders = ["San Ysidro", "Otay Mesa"]
        
        for border in borders:
            image_path = f"{border.lower().replace(' ', '_')}_wait_times.png"
            
            # Create image
            create_border_image(wait_times, border, image_path)
            
            # Post to Facebook
            post_id = post_to_facebook_page(image_path, border)
            
            if post_id:
                logger.info(f"Posted {border} wait times to Facebook with ID: {post_id}")
            else:
                logger.error(f"Failed to post {border} wait times to Facebook")
            
            # Clean up any leftover image
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    logger.info(f"Cleaned up leftover file: {image_path}")
                except OSError as e:
                    logger.error(f"Error cleaning up {image_path}: {e}")
                    
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == '__main__':
    post_border_wait_times()