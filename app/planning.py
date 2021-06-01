import math
import sys

from meta import Path, Point
from routing import Route, RoutePosition
import matplotlib.pyplot as plt

PATH_LENGTH = 3
POINTS_COUNT = 20
MIN_RADIUS = 1

paths = []


def generate_path(radius):
    end_angle = PATH_LENGTH / radius
    first_point = Point(0, 0)
    circle_center = Point(0, -radius)

    points = []

    for i in range(POINTS_COUNT):
        angle = -end_angle / (POINTS_COUNT-1) * i
        point = first_point.get_rotated(angle, circle_center)
        points.append(point)

    path = Path(points)
    path.radius = radius
    return path


def generate_paths():
    for sign in [1, -1]:
        r = MIN_RADIUS * sign
        for i in range(35):
            path = generate_path(r)
            paths.append(path)
            if abs(r) < 6:
                r *= 1.1
            else:
                r *= 1.2


def get_matching_factor(path, points):
    matching_factor = 0

    for point in points:
        offset = path.get_closest_offset(point)
        closest_point = path.get_point_on_path(offset)
        matching_factor += point.get_distance(closest_point)

    return matching_factor


def find_best_path(route: Route, cur_position: RoutePosition, car_gps, car_orientation):
    points = []
    for distance in [2]:
        position, _ = route.add_distance_to_position(cur_position, distance)
        point = route[position].get_point_on_path(position.offset)  # TODO
        print(point, car_gps)
        point.x -= car_gps.x
        point.y -= car_gps.y
        print('#' + str(point))
        # print(point)
        # print(point)
        # print(car_orientation)
        plt.plot(point.x, point.y, 'ro')
        point = point.get_rotated(-car_orientation, Point(0, 0))
        plt.plot(point.x, point.y, 'bo')
        # plt.show()
        points.append(point)
        # sys.exit(0)
    # print(points)

    best_path = None
    best_factor = math.inf

    for path in paths:
        factor = get_matching_factor(path, points)
        if factor < best_factor:
            best_factor = factor
            best_path = path

    return best_path


generate_paths()
