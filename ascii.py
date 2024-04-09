from PIL import Image, ImageDraw
import PIL

def ascii(
        image: PIL.Image,
        font_size: int,
        downscale: int = 1,
        size: tuple[int] = None,
        reversed: bool = False,
        colored: bool = False,
        characters: str = " .-~+*=#%@",
        background: tuple[int] = None,
        bias: float = 0.5
    ) -> PIL.Image:
    """
    Turns an image into ascii art.
    :param image: pillow image
    :param font_size: the size of the characters
    :param downscale: downscales the image and keeps the width/height ratio
    :param size: (width, height) in characters not pixels
    :param mode: L, RGB
    :param reversed: the darkest pixels get the larger characters
    :param characters: custom characters, order them from darkest to brightest
    :param background: the background color, default is the average
    :param bias: (0 to 1) the closer it is to 0 the darker the characters it will choose, opposite happens for 1
    :return: pillow image
    """
    mode = "RGB" if colored else "L"
    size = size or tuple(int(i / downscale) // font_size for i in image.size)
    image = image.resize(size).convert(mode)


    if background is None:
        count = 0
        if mode == "L":
            average = 0

            for pixel in image.getdata():
                average += pixel
                count += 1

            background = int(average / count)
        else:
            average = [0] * (3 if mode == "RGB" else 4)

            for pixel in image.getdata():
                for i, v in enumerate(pixel):
                    average[i] += v
                count += 1


            background = [0] * (3 if mode == "RGB" else 1)
            for c, v in enumerate(average):
                background[c] = int(v / count)

            background = tuple(background)


    ascii_art = Image.new(mode, (size[0] * font_size, size[1] * font_size), color=background)

    draw = ImageDraw.ImageDraw(ascii_art)

    x, y = 0, 0
    for pixel in image.getdata():
        if mode == "L":
            brightness = pixel / 256
        else:
            brightness = sum(pixel) / len(pixel) / 255

        brightness += bias - 0.5
        brightness *= bias + 0.5

        if reversed:
            brightness = 0.99 - brightness

        brightness = max(0, min(0.99, brightness))
        character = characters[int(brightness * len(characters))]
        color = (pixel if colored else 255)

        draw.text((x * font_size + font_size / 4, y * font_size), character, fill=color)

        x += 1
        y += x // size[0]
        x %= size[0]

    return ascii_art