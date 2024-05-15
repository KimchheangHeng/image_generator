import os
from PIL import Image, ImageDraw, ImageFont

def generate_stickers(text, font, fill_color, stroke_color, shadow_color):
    # Get the bounding box of the text
    bbox = font.getbbox(text)

    # Determine image size based on the bounding box
    image_width = bbox[2] - bbox[0] + 20  # Add some padding
    image_height = (bbox[3] - bbox[1]) + 40  # Add some padding

    text_x, text_y = (5, 5)

    # Create a new image with transparent background
    image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    shadow_offset_x, shadow_offset_y = (10, 10)  # Offset for the shadow effect

    for y in range(0, shadow_offset_y, 2):
        for x in range(0, shadow_offset_x, 2):
            # Draw the shadow
            draw.text(
                xy=(text_x + x, text_y + y),
                text=text,
                font=font,
                fill=shadow_color,
            )

    # Draw the text
    draw.text(
        xy=(text_x, text_y),
        text=text,
        font=font,
        fill=fill_color,
        stroke_width=2,
        stroke_fill=stroke_color,
    )

    return image


if __name__ == "__main__":
    # List of words
    # words = ["មកដល់ហើយ!", "លក់ដាច់ជាងគេ!", "កុម្ម៉ង់ឥលូវនេះ!"]
    words = ["Bubi Body Lotion"]

    # Directory for font files
    font_dir = "fonts"

    # Output directory for saving the images
    output_dir = "output_images"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate PNG images for each word
    for word in words:
        for font_file in os.listdir(font_dir):
            if font_file.endswith(".ttf"):
                # Load the font
                font_path = os.path.join(font_dir, font_file)
                font = ImageFont.truetype(font_path, size=72)
                
                image = generate_stickers(
                    text=word,
                    font=font,
                    fill_color=(44, 193, 238),
                    stroke_color=(240, 240, 240),
                    shadow_color=(0, 100, 139),
                )
        
                # Save the image as PNG
                font_name = os.path.splitext(font_file)[0]
                png_file = os.path.join(output_dir, f"{word}_{font_name}.png")
                image.save(png_file)
