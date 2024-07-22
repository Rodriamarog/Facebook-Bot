from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def create_image_with_text(text, filename='output.png', image_size=(800, 800), bg_color=(0, 0, 0), text_color=(222, 213, 49), title_color=(255, 255, 0), font_size=60, title_font_size=70, date_font_size=45, date_color=(255, 255, 255)):
    # Create a new blank image
    img = Image.new('RGB', image_size, color=bg_color)
    d = ImageDraw.Draw(img)

    # Define fonts
    try:
        main_font = ImageFont.truetype("Jersey15-Regular.ttf", font_size)
        title_font = ImageFont.truetype("Jersey15-Regular.ttf", title_font_size)
        date_font = ImageFont.truetype("Jersey15-Regular.ttf", date_font_size)
    except IOError:
        print("Font not found, using default font.")
        main_font = ImageFont.load_default()
        title_font = main_font
        date_font = main_font

    # Split text into lines
    lines = text.split('\n')
    title = lines[0]
    content_lines = lines[1:]

    # Group content lines
    groups = []
    current_group = []
    for line in content_lines:
        if '>>' in line and current_group:
            groups.append(current_group)
            current_group = []
        current_group.append(line)
    if current_group:
        groups.append(current_group)

    # Calculate total height
    title_height = d.textbbox((0, 0), title, font=title_font)[3]
    group_heights = [sum([d.textbbox((0, 0), line, font=main_font)[3] for line in group]) for group in groups]
    total_content_height = sum(group_heights) + (len(groups) - 1) * 40  # 40px spacing between groups
    total_height = title_height + total_content_height + 20  # 20px spacing after title

    # Start drawing from top, leaving space for the date at the bottom
    current_y = (image_size[1] - total_height - date_font_size - 60) / 2  # 60px extra padding

    # Draw title (centered)
    title_width = d.textbbox((0, 0), title, font=title_font)[2]
    d.text(((image_size[0] - title_width) / 2, current_y), title, fill=title_color, font=title_font)
    current_y += title_height + 20  # 20px spacing after title

    # Draw content groups (left-aligned)
    left_margin = 50  # Adjust this value to change the left margin
    for group in groups:
        for line in group:
            d.text((left_margin, current_y), line, fill=text_color, font=main_font)
            current_y += d.textbbox((0, 0), line, font=main_font)[3] + 10  # 10px line spacing within group
        current_y += 30  # 30px extra spacing between groups

    # Add the date and time at the bottom (centered)
    now = datetime.now()
    date_time_text = now.strftime('%d de %B de %Y - %H:%M')
    date_text_width = d.textbbox((0, 0), date_time_text, font=date_font)[2]
    date_x = (image_size[0] - date_text_width) / 2
    date_y = image_size[1] - date_font_size - 10  # 10 pixels from the bottom
    d.text((date_x, date_y), date_time_text, fill=date_color, font=date_font)

    # Save the image
    img.save(filename)
    print(f"Image saved as {filename}")

# Example usage remains the same
if __name__ == '__main__':
    sample_text = """SAN YSIDRO:
All Traffic >>
Vehicles: 1:40
Pedestrians: 0:10
Ready Lanes >>
Vehicles: 1:00
Pedestrians: No Delay
Sentri >>
Vehicles: 0:10"""

    create_image_with_text(sample_text, 'improved_wait_times.png')
    print('Image created successfully!')