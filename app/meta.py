import math
from enum import Enum

import numpy as np

from util import Point


class Sign:

    class Type(Enum):
        STOP = 'SignStop'
        WALKWAY = 'SignWalkway'
        ROUNDABOUT = 'SignRoundabout'
        PARKING = 'SignParking'
        LIMIT = 'SignLimit'
        ONEWAY = 'SignOneWay'
        DEADEND = 'SignDeadEnd'
        TRAFFIC_LIGHTS = 'TrafficLights'

        @classmethod
        def from_text(cls, text):
            for sign_type in list(cls):
                if text.startswith(sign_type.value):
                    return sign_type
            return None

    def __init__(self, raw_meta):
        self.type = Sign.Type.from_text(raw_meta[0].decode("utf-8"))
        self.offset = raw_meta[1]
        self.position = Point(*raw_meta[2])

    @staticmethod
    def create_list(raw_meta_list):
        signs_list = []
        for raw_meta in raw_meta_list:
            sign = Sign(raw_meta)
            signs_list.append(sign)
        return signs_list

    def __repr__(self):
        return f'Sign(type={self.type.name}, offset={self.offset:.2f}, position={self.position})'


class Path:

    def __init__(self, samples):
        self.samples = samples
        self.estimated_length = self._calc_estimated_length()

    def __getitem__(self, offset):
        return self.get_point_on_path(offset)

    @property
    def start(self):
        return self.samples[0]

    @property
    def end(self):
        return self.samples[-1]

    def _calc_estimated_length(self):
        length = 0
        prev_sample = self.samples[0]
        for sample in self.samples[1:]:
            length += prev_sample.get_distance(sample)
            prev_sample = sample
        return length

    def get_point_on_path(self, offset):
        assert 0 <= offset <= 1

        between_index = len(self.samples) * offset
        between_offset = between_index % 1

        prev_index = min(max(math.floor(between_index), 0), len(self.samples)-1)
        next_index = min(math.ceil(between_index), len(self.samples)-1)

        prev_point = self.samples[prev_index]
        next_point = self.samples[next_index]

        this_point = Point.interpolate(prev_point, next_point, between_offset)
        return this_point

    def get_closest_point(self, point: Point):
        closest_offset = 0
        closest_distance = point.get_distance(self.samples[0])

        for offset in np.linspace(0, 1, 100):
            cur_point = self[offset]
            distance = point.get_distance(cur_point)
            if distance < closest_distance:
                closest_offset = offset
                closest_distance = distance

        return closest_offset

    @staticmethod
    def get_angle_between_paths(a, b):
        xa = a.end.x - a.start.x
        ya = a.end.y - a.start.y
        xb = b.end.x - b.start.x
        yb = b.end.y - b.start.y

        angle = math.atan2(yb, xb) - math.atan2(ya, xa)
        if angle > math.pi:
            angle -= 2 * math.pi
        if angle < -math.pi:
            angle += 2 * math.pi
        return angle


class SimPath(Path):

    def __init__(self, raw_meta, structure):
        super().__init__(samples=Point.create_from_list(raw_meta[3]))
        self.handle = raw_meta[0]
        self.length = raw_meta[1]
        self.signs = Sign.create_list(raw_meta[2])
        self.structure = structure
        self.successors = []
        self.predecessors = []

    @staticmethod
    def create_paths_list(raw_meta_list, parent_structure):
        paths_list = []
        for raw_meta in raw_meta_list:
            path = SimPath(raw_meta, parent_structure)
            paths_list.append(path)
        return paths_list

    @staticmethod
    def connect(paths):
        for p1 in paths:
            for p2 in paths:
                if p2 is p1:
                    continue
                if p1.end.get_distance(p2.start) < MetaManager.ACCEPTABLE_POINTS_DISTANCE:
                    p1.successors.append(p2)
                    p2.predecessors.append(p1)
        return paths

    def is_roundabout_entrance(self):
        return isinstance(self.structure, Roundabout) and \
               len(self.predecessors) == 1 and isinstance(self.predecessors[0].structure, Street) and \
               len(self.successors) == 1 and isinstance(self.successors[0].structure, Roundabout)

    def is_roundabout_exit(self):
        return isinstance(self.structure, Roundabout) and \
               len(self.successors) == 1 and isinstance(self.successors[0].structure, Street) and \
               len(self.predecessors) == 1 and isinstance(self.predecessors[0].structure, Roundabout)

    def __repr__(self):
        return f'SimPath({self.start} -> {self.end}, length={self.length:.2f}, successors={len(self.successors)}, signs={self.signs})'


class Roundabout:

    RADIUS = 2.2

    def __init__(self, raw_meta):
        self.name = raw_meta[0].decode("utf-8")
        self.center = Point(*raw_meta[1])
        self.paths = SimPath.create_paths_list(raw_meta[2], self)

    def __repr__(self):
        return f'Roundabout(name={self.name}, center={self.center}, paths={len(self.paths)}'


class Street:

    def __init__(self, raw_meta):
        self.name = raw_meta[0].decode("utf-8")
        self.paths = SimPath.create_paths_list(raw_meta[1], self)

    def __repr__(self):
        return f'Street(name={self.name}, paths={len(self.paths)})'

    def is_oneway(self):
        return len(self.paths) == 1


class Crossing:

    def __init__(self, raw_meta):
        self.name = raw_meta[0].decode("utf-8")
        self.paths = SimPath.create_paths_list(raw_meta[1], self)

    def __repr__(self):
        return f'Crossing(name={self.name}, paths={len(self.paths)})'


class MetaManager:

    ACCEPTABLE_POINTS_DISTANCE = 0.01

    def __init__(self, client):
        self._client = client

        self.roundabouts = []
        self.streets = []
        self.crossings = []
        self.paths = []

        self._fetch_meta()
        SimPath.connect(self.paths)

    def get_path_by_id(self, id):
        matching = [p for p in self.paths if p.handle == id]
        return matching[0] if matching else None

    def get_structure_by_name(self, name):
        structures = [*self.roundabouts, *self.streets, *self.crossings]
        for structure in structures:
            if structure.name == name:
                return structure

    def _fetch_meta(self):
        _, *meta = self._client.simxCallScriptFunction("get_meta@Meta", "sim.scripttype_childscript", [], self._client.simxServiceCall())
        roundabouts_meta, streets_meta, crossings_meta = meta[0]

        for roundabout_meta in roundabouts_meta:
            roundabout = Roundabout(roundabout_meta)
            self.roundabouts.append(roundabout)
            self.paths.extend(roundabout.paths)
            
        for street_meta in streets_meta:
            street = Street(street_meta)
            self.streets.append(street)
            self.paths.extend(street.paths)
            
        for crossing_meta in crossings_meta:
            crossing = Crossing(crossing_meta)
            self.crossings.append(crossing)
            self.paths.extend(crossing.paths)
