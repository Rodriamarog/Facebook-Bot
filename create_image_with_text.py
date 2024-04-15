from PIL import Image, ImageDraw, ImageFont
from scrape_wait_times import scrape_wait_times
import locale
from datetime import datetime

# Set the locale to Spanish (Mexico)
#locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')

def create_image_with_text(text, filename='output.png', image_size=(800, 800), bg_color=(0, 0, 0), text_color=(222, 213, 49), font_size=65, date_font_size=45, date_color=(255, 255, 255)):
    # Create a new blank image
    img = Image.new('RGB', image_size, color=bg_color)
    
    # Get a drawing context
    d = ImageDraw.Draw(img)

    # Define the main font
    try:
        main_font = ImageFont.truetype("Jersey15-Regular.ttf", font_size)
    except IOError:
        print("Main font not found, using default font.")
        main_font = ImageFont.load_default()

    # Define the date font
    try:
        date_font = ImageFont.truetype("Jersey15-Regular.ttf", date_font_size)
    except IOError:
        print("Date font not found, using default font.")
        date_font = ImageFont.load_default()
    
    # Add the main text to the image
    # Calculate the bounding box of the text
    lines = text.split('\n')
    total_text_height = sum([d.textbbox((0, 0), line, font=main_font)[3] for line in lines]) + (len(lines) - 1) * 10
    current_h = (image_size[1] - total_text_height) / 2 - date_font_size * 2  # leave space for the date
    for line in lines:
        text_width, text_height = d.textbbox((0, 0), line, font=main_font)[2:4]
        x = (image_size[0] - text_width) / 2
        d.text((x, current_h), line, fill=text_color, font=main_font)
        current_h += text_height + 10
    
    # Add the date and time at the bottom
    now = datetime.now()
    date_time_text = now.strftime('%d de %B de %Y - %H:%M')
    date_text_width, date_text_height = d.textbbox((0, 0), date_time_text, font=date_font)[2:4]
    date_x = (image_size[0] - date_text_width) / 2
    date_y = image_size[1] - date_text_height - 10  # 10 pixels from the bottom
    d.text((date_x, date_y), date_time_text, fill=date_color, font=date_font)
    
    # Save the image
    img.save(filename)
    print(f"Image saved as {filename}")

# Example usage
if __name__ == '__main__':
    wait_times = scrape_wait_times()
    count = 1
    for wait_time in wait_times:
        text_to_print = '\n'.join(wait_time)
        create_image_with_text(text_to_print, f'wait_times{count}.png')
        count += 1
    
    print('Images created successfully!')
