class PathFollower:

    def __init__(self, car, paths):
        self.car = car
        self.paths = paths
        self.cur_path = paths[0]

    def follow(self):
        self.car.navigate(self.car.target_point)
        if self.car.target_point[0] == self.cur_path.end.x and self.car.target_point[1] == self.cur_path.end.y:
            if not self.paths:
                self.car.target_velocity = 0
            else:
                self.cur_path = self.paths[0]
                self.paths = self.paths[1:]
                self.car.cur_path = self.cur_path.handle
