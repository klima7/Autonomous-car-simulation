from typing import *
from copy import copy
from meta import Path


class RoutePosition:

    def __init__(self, ordinal=0, offset=0):
        self.ordinal = ordinal
        self.offset = offset

    def __iadd__(self, num):
        self.ordinal += num
        return self

    def __index__(self):
        return self.ordinal

    def __repr__(self):
        return f'RoutePosition({self.ordinal}, {self.offset})'


class Route:

    def __init__(self, paths: List[Path] = []):
        self.paths = paths

    def __getitem__(self, item):
        return self.paths[item]

    def __add__(self, other: 'Route'):
        if len(self.paths) != 0 and len(other.paths) != 0 and self[-1] != other[0]:
            raise RuntimeError('Provided routes are not connected, so it is impossible to add them')
        combined_paths = self.paths + other.paths[0:]
        return Route(combined_paths)

    def __iadd__(self, other: 'Route'):
        return self + other

    def __repr__(self):
        text = f'Route('
        for path in self.paths:
            text += str(path) + ", "
        text = text[:-2]
        return text

    def get_distance_between(self, start: RoutePosition, end: RoutePosition):
        return self.get_distance(end) - self.get_distance(start)

    def get_distance(self, end: RoutePosition):
        distance = 0
        for i in range(end.ordinal):
            distance += self.paths[i].length
        distance += self.paths[end.ordinal].length * end.offset
        return distance

    def get_next_position(self, pos: RoutePosition, predicate):
        pos = copy(pos)
        while pos.ordinal < len(self.paths):
            if predicate(self.paths[pos]):
                return pos
            pos.ordinal += 1
            pos.offset = 0
        return None

    def get_prev_position(self, pos: RoutePosition, predicate):
        pos = copy(pos)
        while pos.ordinal >= 0:
            if predicate(self.paths[pos]):
                return pos
            pos.ordinal -= 1
            pos.offset = 1
        return None


class Driver:

    def __init__(self, car):
        self.car = car
        self.route = Route()
        self.position = RoutePosition()

    def add_route(self, route):
        self.route += route

    def drive(self):
        self.position.offset = self.car.cur_path_offset
        self.car.target_velocity = 20

        self.car.navigate(self.car.target_point)
        if self.position.offset == 1:
            self.position += 1
            self.car.cur_path = self.route[self.position].handle

