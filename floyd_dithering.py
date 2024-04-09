from PIL import Image, ImageDraw
import PIL

SECONDARY_DITHER_MATRIX = [[0, 0, 1/16], [7 / 16,  1 / 16, 4 / 16]]

def floyd_dithering(
        image: PIL.Image,
        downscale: int = 1,
        size: tuple[int] = None,
        colored: bool = False,
        bias: float = 0.5,
        colors: int = 1,
        matrix: list[list[float]] = None
    ) -> PIL.Image:
    """
    Applies Floyd-Steinberg dithering to an image.
    :param image: pillow image
    :param downscale: lowers the image quality(optional)
    :param size: new image size(optional)
    :param mode: L, RGB
    :param bias: (0 to 1), closer to 0 is darker, closer to 1 is brighter
    :param colors: the number of colors used
    :param matrix: the weights for the dither, default is [[0, 0, 7 / 16], [3 / 16, 5 / 16, 1 / 16]], first 2 values get ignored
    :return: pillow image
    """
    if matrix is not None:
        if type(matrix) not in [tuple, list]:
            raise ValueError("dither matrix must be a list or tuple")
        if type(matrix[0]) not in [tuple, list]:
            raise ValueError("matrix rows must be list or tuple")
        if len(matrix[0]) != 3 or len(matrix[1]) != 3:
            raise ValueError("dither matrix must be 3x2 (width x height)")

    if type(colors) is not int or colors < 1:
        raise ValueError("'colors' argument must be an integer bigger or equal to 1")

    matrix = matrix or [[0, 0, 7 / 16], [3 / 16, 5 / 16, 1 / 16]]

    mode = "RGB" if colored else "L"
    size = size or tuple(int(i / downscale) for i in image.size)
    image = image.resize(size).convert(mode)

    data = list(image.getdata())

    div = (255 / colors)
    if mode == "L":
        for i, v in enumerate(data):
            new = int(round(v / (div + 1)) * div)

            err = v - new
            data[i] = new

            if (i + 1) % image.width != 0:
                data[i + 1] += int(err * matrix[0][2])
                if i + image.width < image.width * image.height:
                    data[i + 1 + image.width] += int(err * matrix[1][2])

            if i + image.width < image.width * image.height:
                data[i + image.width] += int(err * matrix[1][1])
                if i % image.width != 0:
                    data[i - 1 + image.width] += int(err * matrix[1][0])
    else:
        data = [list(i) for i in data]
        for i, v in enumerate(data):
            new = [int(max(0, min(255, c * (bias * 2))) // div * div) for c in v]
            new = [max(0, min(255, c)) for c in new]

            err = [v[i] - c for i, c in enumerate(new)]

            data[i] = new

            for idx, c in enumerate(err):
                if (i + 1) % image.width != 0:
                    data[i + 1][idx] += int(c * matrix[0][2])
                    if i + image.width < image.width * image.height:
                        data[i + 1 + image.width][idx] += int(c * matrix[1][2])

                if i + image.width < image.width * image.height:
                    data[i + image.width][idx] += int(c * matrix[1][1])
                    if i % image.width != 0:
                        data[i - 1 + image.width][idx] += int(c * matrix[1][0])
        data = [tuple(i) for i in data]

    image.putdata(data)

    return image