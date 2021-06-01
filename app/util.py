import math


class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x:.2f},{self.y:.2f})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_distance(self, point):
        return math.sqrt((self.x-point.x)**2 + (self.y-point.y)**2)

    def get_rotated(self, angle, center):
        s = math.sin(angle)
        c = math.cos(angle)

        x = self.x - center.x
        y = self.y - center.y

        new_x = x * c - y * s
        new_y = x * s + y * c

        new_x += center.x
        new_y += center.y

        return Point(new_x, new_y)

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


def move_forward(start: Point, angle, distance):
    x = start.x + (distance * math.cos(angle))
    y = start.y + (distance * math.sin(angle))
    return Point(x, y)


def get_vector_angle(vector):
    angle = math.atan2(vector[1], vector[0])
    if angle < 0:
        angle += 2*math.pi
    return angle
