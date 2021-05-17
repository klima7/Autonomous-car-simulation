import math
from typing import *
from copy import copy
from meta import Path, Crossing, Roundabout


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

    def __len__(self):
        return len(self.paths)

    def __repr__(self):
        text = f'Route('
        for path in self.paths:
            text += str(path) + ", "
        text = text[:-2]
        return text

    def get_distance_between(self, start: RoutePosition, end: RoutePosition):
        if start is None or end is None:
            return None
        return self.get_distance(end) - self.get_distance(start)

    def get_distance(self, end: RoutePosition):
        if end is None:
            return None
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
        self.car.navigate(self.car.follower.target_point)
        self._adjust_speed()
        self._update_position()

    def _adjust_speed(self):

        def should_slow_down(path):
            return isinstance(path.structure, Crossing) or isinstance(path.structure, Roundabout)

        self.car.steering.target_velocity = 25

        next_crossing_pos = self.route.get_next_position(self.position, should_slow_down)
        next_crossing_distance = self.route.get_distance_between(self.position, next_crossing_pos)
        next_crossing_distance = math.inf if next_crossing_distance is None else next_crossing_distance + 0.4

        prev_crossing_pos = self.route.get_prev_position(self.position, should_slow_down)
        prev_crossing_distance = self.route.get_distance_between(prev_crossing_pos, self.position)
        prev_crossing_distance = math.inf if prev_crossing_distance is None else max(0, prev_crossing_distance - 0.4)

        distance = min(next_crossing_distance, prev_crossing_distance)

        if distance < 1.5:
            self.car.steering.target_velocity = 10

    def _update_position(self):
        self.position.offset = self.car.follower.cur_path_offset
        if self.position.offset == 1:
            if self.position.ordinal + 1 >= len(self.route):
                self.car.steering.target_velocity = 0
            else:
                self.position += 1
                self.car.follower.cur_path = self.route[self.position].handle

