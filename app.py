import re
import os
import shutil
from flask import Flask, request, send_file, render_template
from PIL import ImageFont

from generate_images import generate_images

# Generate the image using the provided parameters (similar to the code in your question)
font_dir = "fonts"
output_dir = "output"

try:
    shutil.rmtree(output_dir)
except Exception:
    pass
os.makedirs(output_dir, exist_ok=True)

app = Flask(__name__, static_folder=output_dir, static_url_path="/")
app.add_url_rule(
    "/output/<path:filename>", endpoint="output", view_func=app.send_static_file
)

def has_contained_khmer_unicode(text):
    khmer_pattern = re.compile(r"[\u1780-\u17FF\u19E0-\u19FF]+")
    return bool(re.search(khmer_pattern, text))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generated_images", methods=["GET", "POST"])
def generated_images():
    text = request.args.get("text")
    if not has_contained_khmer_unicode(text):
       text = "សួស្ដី"

    fill_color = request.args.get("fillColor")
    shadow_color = request.args.get("shadowColor")
    stroke_color = request.args.get("strokeColor")

    for font_file in os.listdir(font_dir):
        if font_file.endswith(".ttf"):
            # Load the font
            font_path = os.path.join(font_dir, font_file)
            font = ImageFont.truetype(font_path, size=72)

            image = generate_images(
                text=text,
                font=font,
                fill_color=fill_color,
                stroke_color=stroke_color,
                shadow_color=shadow_color,
            )

            # Save the image as a PNG
            font_name = os.path.splitext(font_file)[0]
            png_file = os.path.join(output_dir, f"{text}_{font_name}.png")
            image.save(png_file)

    # Create a zip file
    shutil.make_archive(output_dir, "zip", output_dir)

    images = get_generated_images()
    return render_template("generate_images.html", images=images)


@app.route("/download/<path:image_path>")
def download_image(image_path):
    return send_file(image_path, as_attachment=True)


@app.route("/download_all/<path:file_path>")
def download_all(file_path):
    return send_file(file_path, as_attachment=True)


def get_generated_images():
    images = []
    for file in os.listdir(output_dir):
        if file.endswith(".png"):
            image_name = os.path.splitext(file)[0]
            image_path = os.path.join(output_dir, file)
            images.append({"name": image_name, "path": image_path})
    return images


if __name__ == "__main__":
    app.run()
