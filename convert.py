import argparse
from PIL import Image, ImageDraw
import os.path

# Parse args
def validate_img_path(parser, path: str):
    if not os.path.exists(path):
        parser.error("The file %s does not exist!" % path)
    else:
        return Image.open(path)

parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="file", required=True,
                    help="Input path to image.", metavar="FILE",
                    type=lambda x: validate_img_path(parser, x))

parser.add_argument("-o", dest="output", required=True,
                    help="Output path for the image", metavar="FILE")

args = parser.parse_args()

# Settings stuff
gradient = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]
# Mario: 240, 240
# Starry night: 560, 450 (original res)
width = 560
height = 450
maxval = 255
multiplier = 3

# Open image
im = args.file
# Set to grayscale
im = im.convert("L")
# Downsize it
im.thumbnail((width, height), Image.ANTIALIAS)
width, height = im.size

# Get text
res = ""
for y in range(height):
    row = ""
    for x in range(width):
        pixel = im.getpixel((x, y))
        val = pixel
        val = (val/(maxval/100))*(len(gradient)/100)
        row += gradient[int(val)-1]*multiplier
    res += row + "\n"

# Create placeholader image to find out what the resulting text width will be
temp = Image.new('RGB', (1000, 1000), (0, 0, 0))
tempd = ImageDraw.Draw(temp)
w, h = tempd.textsize(res)

# Create the output image
img = Image.new('RGB', (w, h), (0, 0, 0))
d = ImageDraw.Draw(img)
# Draw white text into the image
# fill in RGB
d.text((0, 0), res, fill=(255, 255, 255))
# Save image
img.save(args.output)