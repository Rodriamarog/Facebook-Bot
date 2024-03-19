from PIL import Image, ImageDraw, ImageFont

def create_image_with_text(text, filename='output.png', image_size=(800, 400), bg_color=(255, 255, 255), text_color=(0, 0, 0), font_size=24):
    # Create a new blank image
    img = Image.new('RGB', image_size, color=bg_color)
    
    # Get a drawing context
    d = ImageDraw.Draw(img)
    
    # Define a font (download or choose a path to a .ttf file you have)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # If specific font is not found, PIL will use a default one
        font = ImageFont.load_default()
    
    # Add text to image
    d.text((10, 10), text, fill=text_color, font=font)
    
    # Save the image
    img.save(filename)

# Example usage
if __name__ == '__main__':
    text_content = "San Ysidro Wait Times:\nAll Traffic >> 20 mins\nReady Lanes >> 15 mins\nSentri >> 5 mins"
    create_image_with_text(text_content, 'wait_times.png')
