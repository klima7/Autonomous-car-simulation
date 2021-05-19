import math
import time

from meta import Crossing, Roundabout
from routing import Route, RoutePosition, RouteFinder
from car import Lights


class Driver:

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm

        self.targets = []
        self.route = None
        self.position = None

        self.stop_time = 0

    def add_target(self, target):
        self.targets.append(target)

    def drive(self):
        self.update_route()
        self.follow_route()
        self.update_lights()
        self.update_speed()

    def update_lights(self):
        self.car.lights.running = True

        if self.route is None:
            self.car.lights.indicators = Lights.Indicators.HAZARD_LIGHTS
            return

        next_crossing_pos = self.route.get_next_position(self.position, lambda path: isinstance(path.structure, Crossing) or path.is_roundabout_exit())
        next_crossing_distance = self.route.get_distance_between(self.position, next_crossing_pos)

        prev_crossing_pos = self.route.get_prev_position(self.position, lambda path: isinstance(path.structure, Crossing) or path.is_roundabout_exit())
        prev_crossing_distance = self.route.get_distance_between(prev_crossing_pos, self.position)

        if next_crossing_pos is not None and next_crossing_distance < 2.5:
            angle = self.route.get_angle(next_crossing_pos)
            if angle > 0.2:
                self.car.lights.indicators = Lights.Indicators.LEFT
            elif angle < -0.2:
                self.car.lights.indicators = Lights.Indicators.RIGHT
        if prev_crossing_pos is not None and 3 > prev_crossing_distance > 2:
            self.car.lights.indicators = Lights.Indicators.DISABLED

    def update_speed(self):
        if self.route is None:
            self.car.steering.target_velocity = 0
        else:
            self.car.steering.target_velocity = 20

    def update_route(self):
        if self.route is None:
            if self.targets:
                self.car.lights.indicators = Lights.Indicators.DISABLED
                self.position = RoutePosition(0, self.car.follower.cur_path_offset)
                self.route = RouteFinder.find_route_to_structure(self.mm.get_path_by_id(self.car.follower.cur_path), self.targets[0])

    def follow_route(self):
        if self.route is None:
            return

        self.car.navigate(self.car.follower.target_point)

        self.position.offset = self.car.follower.cur_path_offset
        if self.position.offset == 1:
            if self.position.ordinal + 1 >= len(self.route):
                self.route = None
                self.targets.pop(0)
            else:
                self.position += 1
                self.position.offset = 0
                self.car.follower.cur_path = self.route[self.position].handle
