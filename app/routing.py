from copy import copy
from typing import List
from meta import SimPath


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

    def __eq__(self, other: 'RoutePosition'):
        return self.ordinal == other.ordinal and self.ordinal == other.offset

    def __lt__(self, other: 'RoutePosition'):
        return self.ordinal < other.ordinal or self.ordinal == other.ordinal and self.offset < other.offset


class Route:

    def __init__(self, paths: List[SimPath] = []):
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

    def get_angle(self, pos: RoutePosition):
        if pos.ordinal < 1 or pos.ordinal+1 >= len(self.paths):
            return 0

        prev = self.paths[pos.ordinal-1]
        next = self.paths[pos.ordinal+1]
        return SimPath.get_angle_between_paths(prev, next)

    def get_signs_between(self, pos1: RoutePosition, pos2: RoutePosition):
        signs = []

        # First path
        path = self.paths[pos1.ordinal]
        for sign in path.signs:
            if sign.offset >= pos1.offset and (pos2.ordinal > pos1.ordinal or sign.offset <= pos2.offset):
                signs.append(sign)

        # Middle paths
        for i in range(pos1.ordinal+1, pos2.ordinal):
            path = self.paths[i]
            for sign in path.signs:
                signs.append(sign)

        # Last path
        if pos1.ordinal != pos2.ordinal:
            path = self.paths[pos2.ordinal]
            for sign in path.signs:
                if sign.offset <= pos2.offset:
                    signs.append(sign)

        return signs

    def add_distance_to_position(self, pos: RoutePosition, distance: float):

        cur_pos = copy(pos)

        for path in self.paths[pos.ordinal:]:
            path_reminder_distance = path.length * (1 - cur_pos.offset)
            if path_reminder_distance >= distance:
                cur_pos.offset += distance / path.length
                return cur_pos, 0
            distance -= path_reminder_distance
            cur_pos.ordinal += 1
            cur_pos.offset = 0

        cur_pos.ordinal -= 1
        cur_pos.offset = 1
        return cur_pos, distance


class RouteFinder:

    class PathWrapper:
        def __init__(self, path):
            self.path = path
            self.prev = None

    @staticmethod
    def find_route(start_path, target):
        if isinstance(target, SimPath):
            return RouteFinder.find_route_to_path(start_path, target)
        else:
            return RouteFinder.find_route_to_structure(start_path, target)

    @staticmethod
    def find_route_to_path(start_path, end_path):
        return RouteFinder.find_route_to_path_predicate(start_path, lambda path: path == end_path)

    @staticmethod
    def find_route_to_structure(start_path, end_structure):
        return RouteFinder.find_route_to_path_predicate(start_path, lambda path: path.structure == end_structure)

    @staticmethod
    def find_route_to_path_predicate(start, target_path_predicate):
        routes = RouteFinder._find_routes_to_path(start, target_path_predicate)
        shortest = RouteFinder._find_shortest_route(routes)
        shortest_way = RouteFinder._create_shortest_route(shortest)
        shortest_way = [start, *shortest_way]
        return Route(shortest_way)

    @staticmethod
    def _find_routes_to_path(start, target_path_predicate):
        start = RouteFinder.PathWrapper(start)

        open_list = [start]
        closed_list = []
        routes = []

        while len(open_list) > 0:
            x = open_list.pop(0)
            if target_path_predicate(x.path):
                routes.append(x)
                continue
            closed_list.append(x)
            for neighbor in x.path.successors:
                if neighbor in [item.path for item in closed_list]:
                    continue
                else:
                    t = RouteFinder.PathWrapper(neighbor)
                    t.prev = x
                    open_list.append(t)
        return routes

    @staticmethod
    def _calc_route_length(route):
        length = 0
        r = route.prev
        while True:
            if r is None:
                return length
            length += r.path.length
            r = r.prev

    @staticmethod
    def _find_shortest_route(routes):
        min_length = RouteFinder._calc_route_length(routes[0])
        min_route = routes[0]
        for route in routes:
            length = RouteFinder._calc_route_length(route)
            if length < min_length:
                min_length = length
                min_route = route
        return min_route

    @staticmethod
    def _create_shortest_route(shortest):
        arr = []
        r = shortest
        while r.prev is not None:
            arr.append(r.path)
            r = r.prev
        arr.reverse()
        return arr
