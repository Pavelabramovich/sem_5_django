import numpy as np
from PIL import Image, ImageDraw
import random


def crop_to_square(image, new_size):
    if image.height > image.width:
        resized_image = image.resize((new_size, int(image.height * (new_size / image.width))))

        required_loss = resized_image.height - new_size
        resized_image = resized_image.crop(
            box=(0, required_loss / 2, new_size, resized_image.height - required_loss / 2))

        return resized_image
    else:
        resized_image = image.resize((int(image.width * (new_size / image.height)), new_size))

        required_loss = resized_image.width - new_size
        resized_image = resized_image.crop(
            box=(required_loss / 2, 0, resized_image.width - required_loss / 2, new_size))

        return resized_image


def crop_to_circle(image, new_size):
    image = crop_to_square(image, new_size)

    # Create a transparent black square (color = 0, 0, 0) and draw a
    # white opaque circle in the center (color = 255, 255, 255).
    mask_image = Image.new('RGBA', image.size, color=(0, 0, 0, 0))
    ImageDraw.Draw(mask_image).pieslice(((0, 0), (image.height, image.width)), 0, 360, fill=(255, 255, 255, 255))

    mask_array = np.array(mask_image.convert('RGBA'))
    image_array = np.array(image.convert('RGBA'))

    # Divide all the values by 255 and multiply by the original array.
    # Thus, the white circle will not change the color and transparency in any way, and the black corners
    # will make the corners black and transparent. At the end we convert to int
    circle_array = (image_array * (mask_array / 255)).astype(np.uint8)

    return Image.fromarray(circle_array)


def create_background(size, color):
    if len(color) == 3:
        color = (*color, 255)

    return Image.new('RGBA', size, color=color)


def get_random_color(seed):
    random.seed(seed)
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
