import math
from meta import Crossing, Roundabout
from routing import Route, RoutePosition, RouteFinder
from car import Lights


class Driver:

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm
        self.router = RouteFinder()

        self.targets = []
        self.route = None
        self.position = None

    def add_target(self, target):
        self.targets.append(target)

    def drive(self):
        self.update_route()
        self.follow_route()

    def update_route(self):
        if self.route is None:
            if self.targets:
                self.car.steering.target_velocity = 20
                self.car.lights.indicators = Lights.Indicators.DISABLED
                self.position = RoutePosition(0, self.car.follower.cur_path_offset)
                self.route = self.router.find_route_to_structure(self.mm.get_path_by_id(self.car.follower.cur_path), self.targets[0])

            else:
                self.car.steering.target_velocity = 0
                self.car.lights.indicators = Lights.Indicators.HAZARD_LIGHTS
                return

    def follow_route(self):
        if self.route is None:
            return

        self.car.navigate(self.car.follower.target_point)

        self.position.offset = self.car.follower.cur_path_offset
        if self.position.offset == 1:
            if self.position.ordinal + 1 >= len(self.route):
                self.car.steering.target_velocity = 0
                self.route = None
                self.targets.pop(0)
            else:
                self.position += 1
                self.car.follower.cur_path = self.route[self.position].handle
