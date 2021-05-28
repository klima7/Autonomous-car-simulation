import sys
from copy import copy

from car import Lights
from routing import RoutePosition, RouteFinder
from meta import Path
from time import time


class Driver:

    NORMAL_SPEED = 20
    WALKWAY_SPEED = 8
    LIMITED_SPEED = 10

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm

        self.targets = []
        self.route = None
        self.position = None

        self.cur_path = Path.get_path_closest_to_point(self.mm.paths, self.car.preview_point)
        self.cur_path_offset = None

    def add_target(self, target):
        self.targets.append(target)

    def drive(self):
        self.cur_path_offset = self.cur_path.get_closest_offset(self.car.preview_point)
        # print(self.cur_path_offset, self.car.preview_point, self.cur_path)

        self.update_route()
        self.follow_route()
        self.update_speed()

    def update_speed(self):
        if self.route is None:
            self.car.steering.velocity = 0
        else:
            self.car.steering.velocity = Driver.NORMAL_SPEED

    def update_route(self):
        if self.route is None:
            if self.targets:
                # self.car.lights.indicators = Lights.Indicators.DISABLED
                self.position = RoutePosition(0, self.cur_path_offset)
                # self.prev_position = self.position
                self.route = RouteFinder.find_route_to_structure(self.cur_path, self.targets[0])

    def follow_route(self):
        # self.prev_position = copy(self.position)

        if self.route is None:
            return

        target_offset = self.cur_path.get_closest_offset(self.car.preview_point)
        target_point = self.cur_path[target_offset]

        self.car.navigate(target_point)

        self.position.offset = self.cur_path_offset
        if self.position.offset == 1:
            if self.position.ordinal + 1 >= len(self.route):
                self.route = None
                self.targets.pop(0)
            else:
                self.position += 1
                self.position.offset = 0
                self.cur_path = self.route[self.position]

