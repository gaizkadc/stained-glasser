import os
import random

from PIL import ImageDraw, Image


def create_palette(logger):
    logger.info('creating palette')

    palette = []

    for i in range(int(os.getenv('PALETTE_SIZE'))):
        palette.append(get_random_color(logger))
        logger.info(f'color {i}: {palette[i]}')

    return palette


def draw_triangles(logger, i, triangles, output_folder_path, palette):
    logger.info('drawing triangles')

    x = int(os.getenv('SG_WIDTH'))
    y = int(os.getenv('SG_HEIGHT'))
    img_size = (x, y)

    img_name = f'phase{i}'

    resulting_img_path = output_folder_path + '/' + img_name + '.png'

    img = Image.new('RGB', img_size)

    for triange in triangles:
        draw_single_triangle(logger, img, triange, random.choice(palette))

    img.save(resulting_img_path)

    logger.info(f'image created at {resulting_img_path}')
    return resulting_img_path


def draw_single_triangle(logger, img, triangle, fill_color):
    logger.info('drawing single triangle')

    draw = ImageDraw.Draw(img)

    # draw.polygon(triangle.exterior.coords, fill=fill_color, outline='black')
    draw.polygon(triangle.exterior.coords, fill=fill_color)


def get_random_color(logger):
    logger.info('getting random color')

    return random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)