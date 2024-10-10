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


    partial_sum_matrix = [[[0, ] * 4 for __ in range(image.height)] for _ in range(image.width)]

    for i, v in enumerate(data):
        y, x = divmod(i, image.width)
        partial_sum_matrix[x][y] = list(v)
        if x > 0:
            for g in range(3):
                partial_sum_matrix[x][y][g] += partial_sum_matrix[x - 1][y][g]

        if y > 0:
            for g in range(3):
                partial_sum_matrix[x][y][g] += partial_sum_matrix[x][y - 1][g]
            if x > 0:
                for g in range(3):
                    partial_sum_matrix[x][y][g] -= partial_sum_matrix[x - 1][y - 1][g]


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

                x0 = index % width + x
                y0 = index // width + y

                if x0 >= width:
                    continue
                if y0 >= image.height:
                    continue

                c = abs(min(width - 1, x0 + area) - max(0, x0)) * abs(min(image.height - 1, y0 + area) - max(0, y0))
                for cc in range(3):
                    average[cc] = \
                        partial_sum_matrix[max(0, x0)][max(0, y0)][cc] + partial_sum_matrix[min(width - 1, x0 + area)][min(image.height - 1, y0 + area)][cc] \
                        - partial_sum_matrix[min(width - 1, x0 + area)][max(0, y0)][cc] \
                        - partial_sum_matrix[max(0, x0)][min(image.height - 1, y0 + area)][cc]

                if c != 0:
                    average = [int(gg / c) for gg in average]
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

if __name__ == "__main__":
    image = "rat.png"
    kuwahara(Image.open(image), 1, None, 7).show()
