from meta import Path
from routing import RoutePosition, RouteFinder
from planning import RoutePlanner


class Driver:

    NORMAL_SPEED = 20
    WALKWAY_SPEED = 8
    LIMITED_SPEED = 10

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm
        self.planner = RoutePlanner()

        self.targets = []
        self.route = None
        self.position = None

        self.cur_path = Path.get_path_closest_to_point(self.mm.paths, self.car.preview_point)

    def add_target(self, target):
        self.targets.append(target)

    def drive(self):
        self.update_route()
        self.follow_route()
        self.update_speed()

    def update_speed(self):
        if self.route is None:
            self.car.velocity = 0
        else:
            self.car.velocity = Driver.NORMAL_SPEED

    def update_route(self):
        if self.route is None:
            if self.targets:
                self.position = RoutePosition()
                self.route = RouteFinder.find_route_to_structure(self.cur_path, self.targets[0])

    def follow_route(self):
        if self.route is None:
            return

        planned_path = self.planner.plan_route(self.route, self.position, self.car.gps, self.car.orient)
        planned_target_offset = planned_path.get_closest_offset(self.car.preview_point)
        planned_target_point = planned_path.get_point_on_path(planned_target_offset)
        self.car.navigate(planned_target_point)
        self.car.set_planned_path_visualization(planned_path)

        self.position.offset = self.cur_path.get_closest_offset(self.car.preview_point)
        if self.position.offset == 1:
            if self.position.ordinal + 1 >= len(self.route):
                self.route = None
                self.targets.pop(0)
            else:
                self.position += 1
                self.position.offset = 0
                self.cur_path = self.route[self.position]

