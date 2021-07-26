import os
import random
import math

from shapely.geometry import Point
from shapely.geometry import Polygon


def create_vortices(logger):
    logger.info('creating vortices')

    number_vortices = random.randint(2, 5)
    logger.info(f'number of vortices: {number_vortices}')

    vortices = []
    width = int(os.getenv('SG_WIDTH'))
    height = int(os.getenv('SG_HEIGHT'))

    for i in range(number_vortices):
        vort_x = random.randint(math.floor(0.15 * width),  math.floor(0.85 * width))
        vort_y = random.randint(math.floor(0.15 * height), math.floor(0.85 * height))

        vortices.append(Point(vort_x, vort_y))

        logger.info(f'vortex {i}: [{vort_x}, {vort_y}]')

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
        new_triangle_a = Polygon([Point(0, 0), vortex, Point(x, 0)])
        triangles.append(new_triangle_a)

        new_triangle_b = Polygon([Point(0, 0), vortex, Point(0, y)])
        triangles.append(new_triangle_b)

        new_triangle_c = Polygon([Point(0, y), vortex, Point(x, y)])
        triangles.append(new_triangle_c)

        new_triangle_d = Polygon([vortex, Point(x, 0), Point(x, y)])
        triangles.append(new_triangle_d)

    else:
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
