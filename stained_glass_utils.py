import os
import random

from PIL import ImageDraw, Image

from shapely.geometry import Point
from shapely.geometry import Polygon


def create_vortices(logger):
    logger.info('creating vortices')

    number_vortices = random.randint(4, 8)
    logger.info('number of vortices: ' + str(number_vortices))

    vortices = []

    for i in range(number_vortices):
        vort_x = random.randint(0, int(os.getenv('SG_WIDTH')))
        vort_y = random.randint(0, int(os.getenv('SG_HEIGHT')))

        vortices.append(Point(vort_x, vort_y))

        logger.info(f'vortex {str(i)}: [{str(vort_x)}, {str(vort_y)}]')

    return vortices


def get_triangles(logger, vortex, triangles):
    logger.info('getting triangles')

    x = int(os.getenv('SG_WIDTH'))
    y = int(os.getenv('SG_HEIGHT'))

    if len(triangles) == 0:
        surface = Polygon([Point(0, 0), Point(x, 0), Point(x, y), Point(0, y)])

    else:
        triangle = locate_triangle(logger, vortex, triangles)
        ind = triangles.index(triangle)
        surface = triangles.pop(ind)

    triangles = get_triangles_in_surface(logger, vortex, surface, triangles)

    return triangles


def get_triangles_in_surface(logger, vortex, surface, triangles):
    logger.info('drawing triangles')

    x = int(os.getenv('SG_WIDTH'))
    y = int(os.getenv('SG_HEIGHT'))

    if len(triangles) == 0:
        logger.info('first time here')

        new_triangle_a = Polygon([Point(0, 0), vortex, Point(x, 0)])
        triangles.append(new_triangle_a)

        new_triangle_b = Polygon([Point(0, 0), vortex, Point(0, y)])
        triangles.append(new_triangle_b)

        new_triangle_c = Polygon([Point(0, y), vortex, Point(x, y)])
        triangles.append(new_triangle_c)

        new_triangle_d = Polygon([vortex, Point(x, 0), Point(x, y)])
        triangles.append(new_triangle_d)

    else:
        logger.info('you know the drill')

        surface_list = list(surface.exterior.coords)

        new_triangle_a = Polygon([vortex, surface_list[1], surface_list[2]])
        triangles.append(new_triangle_a)

        new_triangle_b = Polygon([surface_list[0], vortex, surface_list[2]])
        triangles.append(new_triangle_b)

        new_triangle_c = Polygon([surface_list[0], surface_list[1], vortex])
        triangles.append(new_triangle_c)

    print_triangles(logger, triangles)

    return triangles


def locate_triangle(logger, vortex, triangles):
    logger.info('locating triangle')

    for triangle in triangles:
        if triangle.contains(vortex):
            logger.info(f'triangle found: {triangle}')
            return triangle

    logger.info('triangle not found')
    return None


def print_triangles(logger, triangles):
    logger.info('printing triangles')

    for i, triangle in enumerate(triangles):
        logger.info(f'triangle {i}: {triangle}')


def draw_triangles(logger, i, triangles, output_folder_path):
    logger.info('drawing triangles')

    x = int(os.getenv('SG_WIDTH'))
    y = int(os.getenv('SG_HEIGHT'))
    img_size = (x, y)

    img_name = f'phase{i}'

    resulting_img_path = output_folder_path + '/' + img_name + '.png'

    img = Image.new('RGB', img_size)

    for triange in triangles:
        draw_single_triangle(logger, img, triange)

    img.save(resulting_img_path)

    logger.info(f'image created at {resulting_img_path}')
    return resulting_img_path


def draw_single_triangle(logger, img, triangle):
    logger.info('drawing single triangle')

    draw = ImageDraw.Draw(img)

    # draw.polygon(triangle.exterior.coords, fill=get_random_color(logger), outline='white')
    draw.polygon(triangle.exterior.coords, fill=get_random_color(logger))


def get_random_color(logger):
    logger.info('getting random color')

    return random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)
