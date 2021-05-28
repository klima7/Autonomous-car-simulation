from time import time
from copy import copy

import cv2
import numpy as np

from car import Lights
from meta import Crossing, Sign, Point
from routing import RoutePosition, RouteFinder
from enum import Enum, auto


class TrafficLightColor(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()
    NONE = auto()


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
        self.prev_position = None

        self.stop_time = 0
        self.speedup_position = None
        self.speed_limit_street = None

        self.cur_path = self.mm.get_structure_by_name('StreetPaths8').paths[0]

    def add_target(self, target):
        self.targets.append(target)

    def drive(self):
        self.update_route()
        self.follow_route()
        self.update_car_lights()
        self.update_speed()
        self.update_signs()
        self.update_traffic_lights()

    def update_car_lights(self):
        self.car.lights.running = True
        self.car.lights.stop = False

        if self.route is None:
            self.car.lights.indicators = Lights.Indicators.HAZARD_LIGHTS
            return

        next_crossing_pos = self.route.get_next_position(self.position, lambda path: isinstance(path.structure,
                                                                                                Crossing) or path.is_roundabout_exit())
        next_crossing_distance = self.route.get_distance_between(self.position, next_crossing_pos)

        prev_crossing_pos = self.route.get_prev_position(self.position, lambda path: isinstance(path.structure,
                                                                                                Crossing) or path.is_roundabout_exit())
        prev_crossing_distance = self.route.get_distance_between(prev_crossing_pos, self.position)

        if next_crossing_pos is not None and next_crossing_distance < 2.5:
            angle = self.route.get_angle(next_crossing_pos)
            if angle > 0.2:
                self.car.lights.indicators = Lights.Indicators.LEFT
            elif angle < -0.2:
                self.car.lights.indicators = Lights.Indicators.RIGHT
        if prev_crossing_pos is not None and 3 > prev_crossing_distance > 2:
            self.car.lights.indicators = Lights.Indicators.DISABLED

    def update_signs(self):
        if self.route is None:
            return

        signs = self.route.get_signs_between(self.prev_position, self.position)

        for sign in signs:
            if sign.type == Sign.Type.STOP:
                self.stop_time = time()
            if sign.type == Sign.Type.WALKWAY:
                self.speedup_position = self.route.add_distance_to_position(self.position, 2)[0]
            if sign.type == Sign.Type.LIMIT:
                self.speed_limit_street = self.route[self.position].structure

        if self.speed_limit_street is not None:
            self.car.steering.target_velocity = Driver.LIMITED_SPEED
            if self.speed_limit_street != self.route[self.position].structure:
                self.speed_limit_street = None

        if self.speedup_position is not None:
            self.car.steering.target_velocity = Driver.WALKWAY_SPEED
            if self.position > self.speedup_position:
                self.speedup_position = None

        if time() - self.stop_time < 3:
            self.car.steering.target_velocity = 0
            self.car.lights.stop = True

    def update_traffic_lights(self):
        color = self.recognize_light_color()
        if color == TrafficLightColor.RED or color == TrafficLightColor.YELLOW:
            self.car.steering.target_velocity = 0

    def update_speed(self):
        if self.route is None:
            self.car.steering.target_velocity = 0
        else:
            self.car.steering.target_velocity = Driver.NORMAL_SPEED

    def update_route(self):
        if self.route is None:
            if self.targets:
                self.car.lights.indicators = Lights.Indicators.DISABLED
                self.position = RoutePosition(0, self.car.follower.cur_path_offset)
                self.prev_position = self.position
                self.route = RouteFinder.find_route_to_structure(self.cur_path, self.targets[0])

    def follow_route(self):
        self.prev_position = copy(self.position)

        if self.route is None:
            return

        cur_path = self.route[self.position]
        preview_point = self.car.get_preview_point()
        target_offset = cur_path.get_closest_point(preview_point)
        target_point = cur_path[target_offset]

        self.car.navigate(target_point)

        self.position.offset = self.car.follower.cur_path_offset
        if self.position.offset == 1:
            if self.position.ordinal + 1 >= len(self.route):
                self.route = None
                self.targets.pop(0)
            else:
                self.position += 1
                self.position.offset = 0
                self.car.follower.cur_path = self.route[self.position].handle

    def recognize_light_color(self):
        image = self.car.view
        image = image[:, image.shape[1] // 2:]

        lower_red = np.array([0, 150, 20])
        upper_red = np.array([10, 255, 255])

        if Driver.check_light_color(image, lower_red, upper_red):
            return TrafficLightColor.RED

        lower_green = np.array([50, 150, 20])
        upper_green = np.array([80, 255, 255])

        if Driver.check_light_color(image, lower_green, upper_green):
            return TrafficLightColor.GREEN

        lower_yellow = np.array([15, 150, 20])
        upper_yellow = np.array([35, 255, 255])

        if Driver.check_light_color(image, lower_yellow, upper_yellow):
            return TrafficLightColor.YELLOW

        return TrafficLightColor.NONE

    @staticmethod
    def check_light_color(img, lower, upper):
        image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(image, lower, upper)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if (-1 <= w - h <= 1) and cv2.contourArea(contour) > 40:
                return True

        return False
