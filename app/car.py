import math
import util
from api.b0RemoteApi import RemoteApiClient


class Car:

    def __init__(self, client: RemoteApiClient):
        self._client = client

        self.length = 0.316
        self.width = 0.213

        self.gps = None
        self.orient = None

        self.curr_velocity = None
        self.target_velocity = None

        self.curr_left_angle = None
        self.target_left_angle = None

        self.curr_right_angle = None
        self.target_right_angle = None

    def refresh(self):
        _, *data = self._client.simxCallScriptFunction("get_state@Car", "sim.scripttype_childscript", [], self._client.simxServiceCall())
        self.gps = data[0]
        self.orient = data[1][0]
        self.curr_velocity, self.target_velocity = data[2][0:2]
        self.curr_left_angle, self.curr_right_angle = data[2][2]
        self.target_left_angle, self.target_right_angle = data[2][3]

    def apply(self):
        data = [self.target_velocity, self.target_left_angle, self.target_right_angle]
        self._client.simxCallScriptFunction("set_state@Car", "sim.scripttype_childscript", data, self._client.simxDefaultPublisher())

    # positive radius - right, negative - left
    def set_wheels_by_radius(self, radius):
        close_angle = math.atan(self.length / (abs(radius) - self.width/2))
        far_angle = math.atan(self.length / (abs(radius) + self.width / 2))

        if radius < 0:
            left_angle, right_angle = far_angle, close_angle
        else:
            left_angle, right_angle = -close_angle, -far_angle

        self.target_right_angle = left_angle
        self.target_left_angle = right_angle

    # positive angle - right, negative - left
    def set_wheels_by_angle(self, angle):
        radius = self.length / math.tan(util.deg2rad(angle)) if angle != 0 else math.inf
        self.set_wheels_by_radius(radius)