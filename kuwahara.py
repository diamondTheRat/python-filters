from PIL import Image
import PIL
import math


def kuwahara(
        image: PIL.Image,
        downscale: int = 1,
        size: tuple[int] = None,
        area: int = 3,
        mode: str = "RGB"
    ) -> PIL.Image:
    """
    Applies a filter that makes the image look painted.
    THIS IS VERY SLOW.
    :param image: pillow image
    :param downscale: downscales the image
    :param size: the size of the new image
    :param area: the size of the filter(advised is 3)
    :param mode: RGB, RGBA
    :return: pillow image
    """
    if mode not in ["RGB", "RGBA"]:
        raise TypeError("Kuwahara filter only supports RGB and RGBA")

    size = size or tuple(int(i / downscale) for i in image.size)
    image = image.resize(size)
    image = image.convert(mode)

    data = (image.getdata())
    new_data = list(data.copy())

    img_len = image.width * image.height
    width = image.width
    for index, pixel in enumerate(data):
        avg = [255, 255, 255, 0]
        smallest_variance = math.inf
        for x in range(-area, 2, area + 1):
            for y in range(-area, 2, area + 1):
                average = [0, 0, 0, 0]
                count = 0
                variance = 0
                for i in range(area):
                    for j in range(area):
                        idx = index + x + i + (j + y) * width
                        if 0 <= idx and idx < img_len:
                            clr = data[idx]
                            for cc in range(3):
                                average[cc] += clr[cc]
                            count += 1
                if count != 0:
                    average = [int(gg / count) for gg in average]
                    for i in range(area):
                        for j in range(area):
                            idx = index + x + i + (j + y) * width
                            if 0 <= idx and idx < img_len:
                                clr = data[index + x + i + (j + y) * width]
                                for cc in range(3):
                                    variance += (average[cc] - clr[cc]) * (average[cc] - clr[cc])
                    if variance < smallest_variance:
                        smallest_variance = variance
                        avg = average

        new_data[index] = tuple(avg)

    image.putdata(new_data)

    return image