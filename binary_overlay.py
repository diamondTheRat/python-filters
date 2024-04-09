import PIL
from PIL import ImageDraw, ImageFont
from random import randint

def binary_overlay(
        image: PIL.Image,
        font_size: int = 16,
        color_variation: list[int] = [-15, 15],
        flipped: bool = False
    ) -> PIL.Image:

    if font_size % 2 == 1:
        message = "WARNING! using odd numbers for the font size in binary overlay will lead to misaligned text"
        print("-" * len(message))
        print(message)
        print("-" * len(message))

    if type(color_variation) == int:
        color_variation = (color_variation, ) * 2
    elif len(color_variation) != 2:
        raise ValueError("Color variation must be a list or tuple of 2 intergers or an int")

    image = image.convert("RGBA")
    width, height = image.size

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("arial.ttf", font_size)

    down = image.resize((width // int(font_size / 2), height // font_size))
    down = down
    down_width, down_height = down.size

    _data = list(down.getdata())
    for i, pixel in enumerate(_data):
        x, y = i % down_width, i // down_width

        if randint(0, 10) == 0:
            pixel = tuple(i + randint(*color_variation) for i in pixel)

        if flipped:
            x = (down_width - x)
        draw.text((x * (font_size / 2), y * font_size), str(randint(0, 1)), pixel, font)
        
    return image
