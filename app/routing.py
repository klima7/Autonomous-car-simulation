from copy import copy
from typing import List
from meta import SimPath


class Position:

    def __init__(self, reversed=False):
        self.ordinal = 0
        self.offset = 0
        self.reversed = reversed

    def __index__(self):
        return self.ordinal

    def __eq__(self, other: 'Position'):
        return self.ordinal == other.ordinal and self.offset == other.offset

    def __lt__(self, other: 'Position'):
        return self.ordinal < other.ordinal or self.ordinal == other.ordinal and self.get_offset_from_start() < other.get_offset_from_start()

    def get_start_offset(self):
        return 0 if not self.reversed else 1

    def get_end_offset(self):
        return 1 if not self.reversed else 0

    def get_offset_from_start(self):
        return abs(self.get_start_offset() - self.offset)

    def add_offset_from_start(self, add_offset):
        if not self.reversed:
            self.offset += add_offset
        else:
            self.offset -= add_offset

        if self.offset > 1:
            remainder = self.offset - 1
            self.offset = 1
            return remainder

        if self.offset < 0:
            remainder = -self.offset
            self.offset = 0
            return remainder


class Route:

    def __init__(self, paths: List[SimPath] = None, reversed=False):
        self.paths = paths
        self.reversed = reversed

    def __getitem__(self, item):
        return self.paths[item]

    def __len__(self):
        return len(self.paths)

    def get_point(self, pos: Position):
        path = self.paths[pos.ordinal]
        return path.get_point_on_path(pos.offset)

    def add_distance_to_position(self, pos: Position, distance: float):
        cur_pos = copy(pos)

        for path in self.paths[pos.ordinal:]:
            path_reminder_distance = path.length * (1 - cur_pos.get_offset_from_start())
            if path_reminder_distance >= distance:
                cur_pos.add_offset_from_start(distance / path.length)
                return cur_pos, 0
            distance -= path_reminder_distance
            cur_pos.ordinal += 1
            cur_pos.offset = pos.get_start_offset()

        cur_pos.ordinal -= 1
        cur_pos.offset = pos.get_end_offset()
        return cur_pos, distance


class RouteFinder:

    class PathWrapper:
        def __init__(self, path):
            self.path = path
            self.prev = None

    @staticmethod
    def find_route(start_path, target, backward=False):
        if isinstance(target, SimPath):
            return RouteFinder.find_route_to_path(start_path, target, backward)
        else:
            return RouteFinder.find_route_to_structure(start_path, target, backward)

    @staticmethod
    def find_route_to_path(start_path, end_path, backward=False):
        return RouteFinder.find_route_to_path_predicate(start_path, lambda path: path == end_path, backward)

    @staticmethod
    def find_route_to_structure(start_path, end_structure, backward=False):
        return RouteFinder.find_route_to_path_predicate(start_path, lambda path: path.structure == end_structure, backward)

    @staticmethod
    def find_route_to_path_predicate(start, target_path_predicate, backward=False):
        routes = RouteFinder._find_routes_to_path(start, target_path_predicate, backward)
        shortest = RouteFinder._find_shortest_route(routes)
        shortest_way = RouteFinder._create_shortest_route(shortest)
        shortest_way = [start, *shortest_way]
        return Route(shortest_way)

    @staticmethod
    def _find_routes_to_path(start, target_path_predicate, backward=False):
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
            neighbors = x.path.successors if not backward else x.path.predecessors
            for neighbor in neighbors:
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
