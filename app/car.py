from api.b0RemoteApi import RemoteApiClient
import math
import numpy as np


class Car:

    def __init__(self, client: RemoteApiClient):
        self.client = client

        _, self.front_left_wheel = self.client.simxGetObjectHandle('FrontLeftSteerJoint', client.simxServiceCall())
        _, self.front_right_wheel = self.client.simxGetObjectHandle('FrontRightSteerJoint', client.simxServiceCall())
        _, self.back_left_wheel = self.client.simxGetObjectHandle('BackLeftWheelJoint', client.simxServiceCall())
        _, self.back_right_wheel = self.client.simxGetObjectHandle('BackRightWheelJoint', client.simxServiceCall())
        _, self.camera = self.client.simxGetObjectHandle('CarVision1', client.simxServiceCall())
        _, self.body = self.client.simxGetObjectHandle('CarBody', client.simxServiceCall())
        self.width = self.count_distance(self.front_left_wheel, self.front_right_wheel)
        self.length = self.count_distance(self.front_left_wheel, self.back_left_wheel)


    def set_force(self, force):
        self.client.simxSetJointMaxForce(self.back_left_wheel, force, self.client.simxDefaultPublisher())
        self.client.simxSetJointMaxForce(self.back_right_wheel, force, self.client.simxDefaultPublisher())

    def set_angle(self, angle):
        self.client.simxSetJointTargetPosition(self.front_left_wheel, self.to_radians(angle), self.client.simxDefaultPublisher())
        self.client.simxSetJointTargetPosition(self.front_right_wheel, self.to_radians(angle), self.client.simxDefaultPublisher())

    def set_right_angle(self, angle):
        self.client.simxSetJointTargetPosition(self.front_right_wheel, angle,
                                               self.client.simxDefaultPublisher())

    def set_left_angle(self, angle):
        self.client.simxSetJointTargetPosition(self.front_left_wheel, angle,
                                               self.client.simxDefaultPublisher())

    def set_velocity(self, velocity):
        self.client.simxSetJointTargetVelocity(self.back_left_wheel, velocity, self.client.simxDefaultPublisher())
        self.client.simxSetJointTargetVelocity(self.back_right_wheel, velocity, self.client.simxDefaultPublisher())

    def get_camera_image(self):
        _, size, data = self.client.simxGetVisionSensorImage(self.camera, False, self.client.simxServiceCall())
        data = [x for x in data]
        image = np.array(data, dtype=np.uint8)
        image.resize([size[1], size[0], 3])
        return image

    def count_vector_distance(self, vector1, vector2):
        return math.sqrt(((vector2[0]-vector1[0])**2)+((vector2[1]-vector1[1])**2)+((vector2[1]-vector1[1])**2))

    def count_distance(self, obj1, obj2):
        _, left_position = self.client.simxGetObjectPosition(obj1, -1, self.client.simxServiceCall())
        _, right_position = self.client.simxGetObjectPosition(obj2, -1, self.client.simxServiceCall())
        return self.count_vector_distance(left_position, right_position)

    @staticmethod
    def to_radians(degrees):
        return degrees * math.pi / 180
