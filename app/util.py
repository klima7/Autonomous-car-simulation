import math


class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x:.2f},{self.y:.2f})'

    def get_distance(self, point):
        return math.sqrt((self.x-point.x)**2 + (self.y-point.y)**2)


def deg2rad(degrees):
    return degrees * math.pi / 180


def rad2deg(radians):
    return radians * 180 / math.pi
