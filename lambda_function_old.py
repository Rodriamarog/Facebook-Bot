import os
from dotenv import load_dotenv
from scrape_wait_times import get_wait_times  # Changed this import
from create_image_with_text import create_image_with_text
from post_to_facebook import post_to_facebook_page
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_bot():
    # Load environment variables
    load_dotenv()
    
    # Scrape wait times
    wait_times = get_wait_times()  # Changed this function call
    
    if wait_times is None:
        logger.error("Failed to scrape wait times")
        return

    count = 1
    for wait_time in wait_times:
        # Create image
        text_to_print = '\n'.join(wait_time)
        image_path = f'/tmp/wait_times{count}.png'  # Changed to use /tmp directory
        create_image_with_text(text_to_print, image_path)
        
        # Post to Facebook
        result = post_to_facebook_page(image_path, wait_time)
        if result:
            logger.info(f"Posted to Facebook with ID: {result}")
        else:
            logger.error("Failed to post to Facebook")
        
        count += 1

    # Check for any leftover image files and delete them
    for i in range(1, count):
        leftover_image = f'/tmp/wait_times{i}.png'  # Changed to use /tmp directory
        if os.path.exists(leftover_image):
            try:
                os.remove(leftover_image)
                logger.info(f"Deleted leftover file: {leftover_image}")
            except OSError as e:
                logger.error(f"Error deleting leftover file {leftover_image}: {e}")

    logger.info("Bot execution completed")

def lambda_handler(event, context):
    try:
        run_bot()
        return {
            'statusCode': 200,
            'body': 'Bot run successfully'
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': f'Error occurred: {str(e)}'
        }

# This allows you to run the script locally for testing
if __name__ == "__main__":
    run_bot()