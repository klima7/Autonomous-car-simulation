from meta import Path
from routing import Position, RouteFinder
from planning import RoutePlanner
from visual import TrafficLightColor, recognize_light_color


class Task:

    def __init__(self, target, offset=1.0, backward=False):
        self.type = type
        self.target = target
        self.offset = offset
        self.backward = backward


class Driver:

    NORMAL_SPEED = 20
    BACKWARD_SPEED = 20
    WALKWAY_SPEED = 8
    LIMITED_SPEED = 10

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm
        self.planner = RoutePlanner()

        self.tasks = []
        self.cur_task = None

        self.route = None
        self.position = None

        self.cur_path = Path.get_path_closest_to_point(self.mm.paths, self.car.gps)

    def drive_to_structure(self, structure_name, backward=False):
        structure = self.mm.get_structure_by_name(structure_name)
        task = Task(structure, 0.5, backward)
        self.tasks.append(task)

    def drive_to_path(self, path_name, offset, backward=False):
        path = self.mm.get_path_by_name(path_name)
        task = Task(path, offset, backward)
        self.tasks.append(task)

    def update(self):
        self.update_task()
        self.follow_route()
        self.update_speed()
        self.update_traffic_lights()

    def update_task(self):
        if self.cur_task is None:
            if self.tasks:
                self.cur_task = self.tasks.pop(0)
                self.position = Position(reversed=self.cur_task.backward)
                self.route = RouteFinder.find_route(self.cur_path, self.cur_task.target, backward=self.cur_task.backward)

    def update_speed(self):
        if self.cur_task is None:
            self.car.velocity = 0
        elif self.cur_task.backward:
            self.car.velocity = -self.BACKWARD_SPEED
        else:
            self.car.velocity = self.NORMAL_SPEED

    def follow_route(self):
        if self.cur_task is None:
            return

        leading_point = self.car.front_point if not self.cur_task.backward else self.car.back_point
        self.position.offset = self.cur_path.get_closest_offset(leading_point)

        path, radius = self.planner.plan_route(self.route, self.position, leading_point, self.car.orient, backward=self.cur_task.backward)
        self.car.set_wheels_by_radius(radius if not self.cur_task.backward else -radius)
        self.car.set_planned_path_visualization(path)

        if self.cur_path == self.route[len(self.route) - 1] and self.position.get_offset_from_start() >= self.cur_task.offset:   # TODO
            self.cur_task = None

        elif self.position.offset == self.position.get_end_offset():
            self.position.ordinal += 1
            self.position.offset = self.position.get_start_offset()
            self.cur_path = self.route[self.position]

    def update_traffic_lights(self):
        if self.cur_task is None or self.cur_task.backward:
            return

        color = recognize_light_color(self.car.view)
        if color == TrafficLightColor.RED or color == TrafficLightColor.YELLOW:
            self.car.velocity = 0
