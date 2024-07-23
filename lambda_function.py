import os
from dotenv import load_dotenv
from scrape_wait_times import scrape_wait_times
from create_image_with_text import create_image_with_text
from post_to_facebook import post_to_facebook_page

def run_bot():
    # Load environment variables
    load_dotenv()

    # Scrape wait times
    wait_times = scrape_wait_times()

    count = 1
    for wait_time in wait_times:
        # Create image
        text_to_print = '\n'.join(wait_time)
        image_path = f'wait_times{count}.png'
        create_image_with_text(text_to_print, image_path)

        # Post to Facebook
        result = post_to_facebook_page(image_path, wait_time)
        if result:
            print(f"Posted to Facebook with ID: {result}")
        else:
            print("Failed to post to Facebook")

        count += 1

    # Check for any leftover image files and delete them
    for i in range(1, count):
        leftover_image = f'wait_times{i}.png'
        if os.path.exists(leftover_image):
            try:
                os.remove(leftover_image)
                print(f"Deleted leftover file: {leftover_image}")
            except OSError as e:
                print(f"Error deleting leftover file {leftover_image}: {e}")

    print("Bot execution completed")

def lambda_handler(event, context):
    try:
        run_bot()
        return {
            'statusCode': 200,
            'body': 'Bot run successfully'
        }
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error occurred: {str(e)}'
        }

# This allows you to run the script locally for testing
if __name__ == "__main__":
    run_bot()