import math


class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x:.2f},{self.y:.2f})'

    def get_distance(self, point):
        return math.sqrt((self.x-point.x)**2 + (self.y-point.y)**2)

    @staticmethod
    def create_from_list(pos_list):
        points = []
        for pos in pos_list:
            point = Point(pos[0], pos[1])
            points.append(point)
        return points

    @staticmethod
    def interpolate(p1, p2, offset_from_p1):
        x = (1-offset_from_p1) * p1.x + offset_from_p1 * p2.x
        y = (1-offset_from_p1) * p1.y + offset_from_p1 * p2.y
        return Point(x, y)


def deg2rad(degrees):
    return degrees * math.pi / 180


def rad2deg(radians):
    return radians * 180 / math.pi
