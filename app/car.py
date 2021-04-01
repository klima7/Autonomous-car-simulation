from api.b0RemoteApi import RemoteApiClient
import numpy as np
import app.util as util
import math


class Car:

    def __init__(self, client: RemoteApiClient):
        self.client = client

        _, self.front_left_wheel = self.client.simxGetObjectHandle('FLSteerJoint', client.simxServiceCall())
        _, self.front_right_wheel = self.client.simxGetObjectHandle('FRSteerJoint', client.simxServiceCall())
        _, self.back_left_wheel = self.client.simxGetObjectHandle('BLWheelJoint', client.simxServiceCall())
        _, self.back_right_wheel = self.client.simxGetObjectHandle('BRWheelJoint', client.simxServiceCall())
        _, self.camera = self.client.simxGetObjectHandle('CarVision', client.simxServiceCall())

        self.width = util.calc_distance(self.client, self.front_left_wheel, self.front_right_wheel)
        self.length = util.calc_distance(self.client, self.front_left_wheel, self.back_left_wheel)

    def set_force(self, force):
        self.client.simxSetJointMaxForce(self.back_left_wheel, force, self.client.simxDefaultPublisher())
        self.client.simxSetJointMaxForce(self.back_right_wheel, force, self.client.simxDefaultPublisher())

    def set_velocity(self, velocity):
        self.client.simxSetJointTargetVelocity(self.back_left_wheel, velocity, self.client.simxDefaultPublisher())
        self.client.simxSetJointTargetVelocity(self.back_right_wheel, velocity, self.client.simxDefaultPublisher())

    # Ustawia koła zgodnie z podanym promieniem skrętu. Kąt dodatni w prawo, ujemny w lewo
    def set_wheels_by_radius(self, radius):

        close_angle = math.atan(self.length / (abs(radius) - self.width/2))
        far_angle = math.atan(self.length / (abs(radius) + self.width / 2))

        if radius < 0:
            left_angle, right_angle = far_angle, close_angle
        else:
            left_angle, right_angle = -close_angle, -far_angle

        self.client.simxSetJointTargetPosition(self.front_right_wheel, left_angle, self.client.simxDefaultPublisher())
        self.client.simxSetJointTargetPosition(self.front_left_wheel, right_angle, self.client.simxDefaultPublisher())

    # Ustawia koła pod podanym kątem (około). Kąt dodatni w prawo, ujemny w lewo
    def set_wheels_by_angle(self, angle):
        radius = self.length / math.tan(util.deg2rad(angle)) if angle != 0 else math.inf
        self.set_wheels_by_radius(radius)

    def get_camera_image(self):
        _, size, data = self.client.simxGetVisionSensorImage(self.camera, False, self.client.simxServiceCall())
        data = [x for x in data]
        image = np.array(data, dtype=np.uint8)
        image.resize([size[1], size[0], 3])
        return image
