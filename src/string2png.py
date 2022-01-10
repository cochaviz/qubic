from PIL import Image, ImageDraw, ImageFont
import io

font = ImageFont.truetype("assets/Verdana.ttf", 80)


def str2png(string='hello', img_width=200, img_height=200):
    # create png with white background
    img = Image.new('RGB', (img_width, img_height), (255, 250, 255))

    d = ImageDraw.Draw(img)
    text_width, text_height = font.getsize(string)

    # write text on center of image
    d.text(((img_width - text_width) / 2, (img_height - text_height) / 2),
           string, font=font, fill=(0, 0, 0))

    return img
