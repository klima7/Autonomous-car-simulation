import math
import util
from enum import Enum
from api.b0RemoteApi import RemoteApiClient


class Lights:

    class Indicators(Enum):
        DISABLED = 0
        LEFT = 1
        RIGHT = 2
        HAZARD_LIGHTS = 3

    def __init__(self):
        self.indicators = Lights.Indicators.DISABLED
        self.stop = False
        self.running = False
        self.reverse = False

    def get_vector(self):
        return [self.indicators.value, int(self.stop), int(self.running), int(self.reverse)]

    def set_vector(self, vector):
        self.indicators = Lights.Indicators(vector[0])
        self.stop = bool(vector[1])
        self.running = bool(vector[2])
        self.reverse = bool(vector[3])


class AckermanSteering:

    TURNING_ANGLE = 30

    def __init__(self):
        self.curr_velocity = 0
        self.target_velocity = 0

        self.curr_left_angle = 0
        self.target_left_angle = 0

        self.curr_right_angle = 0
        self.target_right_angle = 0

    def get_vector(self):
        return [self.target_velocity, self.target_left_angle, self.target_right_angle]

    def set_vector(self, vector):
        self.curr_velocity, self.target_velocity = vector[0:2]
        self.curr_left_angle, self.curr_right_angle = vector[2]
        self.target_left_angle, self.target_right_angle = vector[3]

    def set_wheels_by_radius(self, radius):
        """positive radius - right, negative - left"""
        close_angle = math.atan(Car.LENGTH / (abs(radius) - Car.WIDTH/2))
        far_angle = math.atan(Car.LENGTH / (abs(radius) + Car.WIDTH / 2))

        if radius < 0:
            left_angle, right_angle = far_angle, close_angle
        else:
            left_angle, right_angle = -close_angle, -far_angle

        self.target_right_angle = left_angle
        self.target_left_angle = right_angle

    def set_wheels_by_angle(self, angle):
        """positive angle - right, negative - left"""
        radius = Car.LENGTH / math.tan(util.deg2rad(angle)) if angle != 0 else math.inf
        self.set_wheels_by_radius(radius)


class Follower:

    def __init__(self):
        self.target_point = None
        self.cur_path = None
        self.cur_path_offset = None
        self.closest_path = None

    def get_vector(self):
        return self.cur_path

    def set_vector(self, vector):
        self.target_point = vector[0]
        self.cur_path = vector[1]
        self.cur_path_offset = vector[2]
        self.closest_path = vector[3]


class Car:
    
    LENGTH = 0.316
    WIDTH = 0.213

    def __init__(self, client: RemoteApiClient):
        self._client = client

        self.gps = None
        self.orient = None

        self.follower = Follower()
        self.steering = AckermanSteering()
        self.lights = Lights()

    def refresh(self):
        _, *data = self._client.simxCallScriptFunction("get_state@Car", "sim.scripttype_childscript", [], self._client.simxServiceCall())
        self.gps = data[0]
        self.orient = data[1]
        self.steering.set_vector(data[2])
        self.follower.set_vector(data[3])
        self.lights.set_vector(data[4])

    def apply(self):
        data = [self.steering.get_vector(), self.follower.get_vector(), self.lights.get_vector()]
        self._client.simxCallScriptFunction("set_state@Car", "sim.scripttype_childscript", data, self._client.simxServiceCall())

    def navigate(self, target):
        diff = [self.gps[0] - target[0], self.gps[1] - target[1]]
        target_angle = util.rad2deg(math.atan2(diff[1], diff[0]) + math.pi)
        car_angle = util.rad2deg(self.orient + math.pi)
        diff_angle = car_angle - target_angle

        if diff_angle > 180:
            diff_angle = 180 - diff_angle
        if diff_angle < -180:
            diff_angle = 360 + diff_angle

        diff_angle = min(self.steering.TURNING_ANGLE, diff_angle)
        diff_angle = max(-self.steering.TURNING_ANGLE, diff_angle)

        self.steering.set_wheels_by_angle(diff_angle)
