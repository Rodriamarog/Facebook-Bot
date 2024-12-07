from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz
import os
import requests

def download_font():
    """Download Inter font if not present"""
    font_path = os.path.join(os.path.dirname(__file__), 'Inter-Regular.ttf')
    font_bold_path = os.path.join(os.path.dirname(__file__), 'Inter-Bold.ttf')
    
    if not os.path.exists(font_path):
        url = "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.ttf"
        response = requests.get(url)
        with open(font_path, 'wb') as f:
            f.write(response.content)
            
    if not os.path.exists(font_bold_path):
        url = "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Bold.ttf"
        response = requests.get(url)
        with open(font_bold_path, 'wb') as f:
            f.write(response.content)
            
    return font_path, font_bold_path

def create_border_image(wait_times, border_type, filename=None):
    """Create image for either San Ysidro or Otay"""
    if filename is None:
        filename = f'{border_type.lower().replace(" ", "_")}_wait_times.png'
        
    # Modern color scheme
    COLORS = {
        'background': (23, 23, 23),    # Dark background
        'title': (255, 255, 255),      # White
        'category': (0, 122, 255),     # Bright blue
        'text': (255, 255, 255),       # White
        'long_wait': (255, 69, 58),    # Red for long waits
        'date': (179, 179, 179)        # Light gray
    }
    
    # Image settings - more compact
    IMAGE_SIZE = (800, 600)  # Reduced size
    PADDING = 40
    LINE_HEIGHT = 50  # Reduced line height
    
    # Get fonts
    regular_font_path, bold_font_path = download_font()
    
    # Create fonts - adjusted sizes
    title_font = ImageFont.truetype(bold_font_path, 56)
    category_font = ImageFont.truetype(bold_font_path, 48)
    main_font = ImageFont.truetype(regular_font_path, 42)
    time_font = ImageFont.truetype(bold_font_path, 42)
    date_font = ImageFont.truetype(regular_font_path, 32)
    
    # Create image
    img = Image.new('RGB', IMAGE_SIZE, COLORS['background'])
    draw = ImageDraw.Draw(img)
    
    # Current Y position
    current_y = PADDING

    # Draw title
    title = f"{border_type}"
    draw.text((PADDING, current_y), title, COLORS['title'], font=title_font)
    current_y += 80  # Reduced spacing after title
    
    # Prepare data based on border type
    prefix = "San Ysidro" if border_type == "San Ysidro" else "Otay"
    
    # Draw Vehicles section
    draw.text((PADDING, current_y), "Vehicles:", COLORS['category'], font=category_font)
    current_y += 60
    
    vehicle_data = [
        ("Regular", wait_times[f"{prefix} All Traffic"]),
        ("Ready Lane", wait_times[f"{prefix} Ready Lane"]),
        ("SENTRI", wait_times[f"{prefix} Sentri"])
    ]
    
    for label, time in vehicle_data:
        text = f"{label}: "
        text_width = draw.textlength(text, font=main_font)
        draw.text((PADDING, current_y), text, COLORS['text'], font=main_font)
        
        time_text = f"{time} min"
        time_color = COLORS['long_wait'] if time > 45 else COLORS['text']
        draw.text((PADDING + text_width, current_y), time_text, time_color, font=time_font)
        current_y += LINE_HEIGHT
    
    current_y += 20  # Space between sections
    
    # Draw Pedestrians section
    draw.text((PADDING, current_y), "Pedestrians:", COLORS['category'], font=category_font)
    current_y += 60
    
    # Modified pedestrian data section to handle different borders
    if border_type == "San Ysidro":
        pedestrian_data = [
            ("Regular", wait_times[f"{prefix} Pedestrian"]),
            ("Ready Lane", wait_times[f"{prefix} Pedestrian Ready"])
        ]
    else:  # Otay Mesa
        pedestrian_data = [
            ("Regular", wait_times[f"{prefix} Pedestrian"])
        ]
    
    for label, time in pedestrian_data:
        text = f"{label}: "
        text_width = draw.textlength(text, font=main_font)
        draw.text((PADDING, current_y), text, COLORS['text'], font=main_font)
        
        time_text = f"{time} min"
        time_color = COLORS['long_wait'] if time > 30 else COLORS['text']
        draw.text((PADDING + text_width, current_y), time_text, time_color, font=time_font)
        current_y += LINE_HEIGHT
    
    # Draw date at bottom
    tijuana_tz = pytz.timezone('America/Tijuana')
    current_time = datetime.now(tijuana_tz)
    date_text = current_time.strftime('%B %d, %Y - %H:%M')
    text_width = draw.textlength(date_text, font=date_font)
    draw.text(
        (IMAGE_SIZE[0] - PADDING - text_width, IMAGE_SIZE[1] - PADDING - 30),
        date_text,
        COLORS['date'],
        font=date_font
    )
    
    # Save image
    img.save(filename)
    print(f"Image saved as {filename}")

def create_both_border_images(wait_times):
    """Create both San Ysidro and Otay images"""
    create_border_image(wait_times, "San Ysidro", "san_ysidro_wait_times.png")
    create_border_image(wait_times, "Otay Mesa", "otay_wait_times.png")

def main():
    sample_wait_times = {
        "San Ysidro All Traffic": 75,
        "San Ysidro Ready Lane": 75,
        "San Ysidro Sentri": 15,
        "San Ysidro Pedestrian": 15,
        "San Ysidro Pedestrian Ready": 1,
        "Otay All Traffic": 45,
        "Otay Ready Lane": 45,
        "Otay Sentri": 10,
        "Otay Pedestrian": 30,
        "Otay Pedestrian Ready": 0
    }
    
    create_both_border_images(sample_wait_times)

if __name__ == "__main__":
    main()