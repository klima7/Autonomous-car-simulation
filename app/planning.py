import math
import numpy as np

from meta import Path, Point


class RoutePlanner:

    PATH_LENGTH = 1
    POINTS_COUNT = 20
    MIN_RADIUS = 0.5
    COMPARISON_DISTANCES_COUNT = 10

    def __init__(self):
        self.paths = self._generate_paths()
        self.comparison_points = self._generate_comparison_points()

    def plan_route(self, route, route_position, leading_point, car_orientation, backward=False):
        points = []
        rotation_angle = car_orientation if not backward else car_orientation + math.pi
        for distance in self.comparison_points:
            position, _ = route.add_distance_to_position(route_position, distance)
            point = route.get_point(position)
            point.x -= leading_point.x
            point.y -= leading_point.y
            point = point.get_rotated(-rotation_angle, Point(0, 0))
            points.append(point)

        best_path = None
        best_factor = math.inf

        for path in self.paths:
            factor = self._compare_path(path, points)
            if factor < best_factor:
                best_factor = factor
                best_path = path

        radius = best_path.radius

        best_path = best_path.get_rotated(rotation_angle, Point(0, 0))
        best_path = best_path.get_translated(leading_point)

        return best_path, radius

    def _generate_comparison_points(self):
        points = np.linspace(0, self.PATH_LENGTH, self.COMPARISON_DISTANCES_COUNT + 1)[1:]
        return points.tolist()

    def _generate_paths(self):
        paths = []
        for sign in [1, -1]:
            r = self.MIN_RADIUS * sign
            for i in range(50):
                path = self._generate_path(r)
                paths.append(path)
                if abs(r) < 6:
                    r *= 1.1
                else:
                    r *= 1.2
        return paths

    def _generate_path(self, radius):
        end_angle = self.PATH_LENGTH / radius
        first_point = Point(0, 0)
        circle_center = Point(0, -radius)

        points = []

        for i in range(self.POINTS_COUNT):
            angle = -end_angle / (self.POINTS_COUNT - 1) * i
            point = first_point.get_rotated(angle, circle_center)
            points.append(point)

        path = Path(points)
        path.radius = radius
        return path

    def _compare_path(self, path, points):
        cumulated_distances = 0
        last_closest_offset = path.get_closest_offset(points[-1])

        for i in range(self.COMPARISON_DISTANCES_COUNT):
            offset = (i+1) / self.COMPARISON_DISTANCES_COUNT
            offset *= last_closest_offset
            point = path.get_point_on_path(offset)
            cumulated_distances += point.get_distance(points[i])

        return cumulated_distances
