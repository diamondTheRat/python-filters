import PIL
from PIL import ImageFilter

def gaussian_blur(
        image: PIL.Image,
        radius: int = 1,
    ) -> PIL.Image:
    """
    Gaussian blur what else do u expect.
    :param image: pillow image
    :param radius: the radius(square) of the blur
    :return: pillow image
    """

    data = image.getdata()
    if image.mode == "L":
        pass
    else:
        blurred = list(image.getdata())
        for i, pixel in enumerate(data):
            average = [0] * (3 + (image.mode == "RGBA"))

            Ox, Oy = i % image.width, i // image.width

            nr = 0
            for y in range(Oy - radius, Oy + radius + 1):
                if y < 0 or y >= image.height: continue
                for x in range(Ox - radius, Ox + radius + 1):
                    if x < 0 or x >= image.width: continue
                    for idx, v in enumerate(average):
                        average[idx] += data[x + y * image.width][idx]
                    nr += 1

            average = tuple(int(i / nr) for i in average)
            blurred[i] = average

    image.putdata(blurred)

    return image

def fast_blur(
        image: PIL.Image,
        intensity: int = 5,
    ) -> PIL.Image:
    """
    Basic blur, it's fast, but it reduces image quality :c
    :param image: pillow image
    :param intensity: how intense the blur is
    :return: pillow image
    """
    size = image.size
    image = image.resize((image.width // intensity, image.height // intensity))
    image = image.resize(size)

    return image