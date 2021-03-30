import math


def deg2rad(degrees):
    return degrees * math.pi / 180


def calc_vectors_distance(vector1, vector2):
    return math.sqrt(sum([(v1-v2)**2 for v1, v2 in zip(vector1, vector2)]))


def calc_distance(client, obj1, obj2):
    _, obj1_position = client.simxGetObjectPosition(obj1, -1, client.simxServiceCall())
    _, obj2_position = client.simxGetObjectPosition(obj2, -1, client.simxServiceCall())
    return calc_vectors_distance(obj1_position, obj2_position)