from meta import Path
from routing import RoutePosition, RouteFinder
from planning import RoutePlanner
from visual import TrafficLightColor, recognize_light_color


class Task:

    def __init__(self, target, offset=1.0, backward=False):
        self.type = type
        self.target = target
        self.offset = offset
        self.backward = backward


class Driver:

    NORMAL_SPEED = 25
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

    def drive(self):
        self.update_task()
        self.follow_route()
        self.update_speed()
        self.update_traffic_lights()

    def update_speed(self):
        if self.cur_task is None:
            self.car.velocity = 0
        else:
            self.car.velocity = Driver.NORMAL_SPEED

    def update_task(self):
        if self.cur_task is None:
            if self.tasks:
                self.cur_task = self.tasks.pop(0)
                self.position = RoutePosition()
                self.route = RouteFinder.find_route(self.cur_path, self.cur_task.target)

    def follow_route(self):
        if self.cur_task is None:
            return

        path, radius = self.planner.plan_route(self.route, self.position, self.car.gps, self.car.orient)
        self.car.set_wheels_by_radius(radius)
        self.car.set_planned_path_visualization(path)

        self.position.offset = self.cur_path.get_closest_offset(self.car.gps)

        if self.cur_path == self.route[len(self.route) - 1] and self.position.offset >= self.cur_task.offset:
            self.cur_task = None

        elif self.position.offset == 1:
            self.position += 1
            self.position.offset = 0
            self.cur_path = self.route[self.position]

    def update_traffic_lights(self):
        color = recognize_light_color(self.car.view)
        if color == TrafficLightColor.RED or color == TrafficLightColor.YELLOW:
            self.car.velocity = 0
