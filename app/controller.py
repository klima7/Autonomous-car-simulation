from pathfinder import PathFinder


class Controller:

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm

    def start(self):
        self.car.refresh()
        self.car.cur_path = self.car.closest_path
        self.car.apply()

        start = self.mm.get_path_by_id(self.car.closest_path)
        end = self.mm.get_path_by_id(1266)

        navigator = PathFinder()
        paths_ahead = navigator.find_path(start, end)

        path = start
        print(path, path.structure)

        while True:
            self.car.refresh()
            self.car.navigate(self.car.target_point)
            if self.car.target_point[0] == path.end.x and self.car.target_point[1] == path.end.y:
                if not paths_ahead:
                    self.car.target_velocity = 0
                else:
                    path = paths_ahead[0]
                    paths_ahead = paths_ahead[1:]
                    self.car.cur_path = path.handle
                    print(path, path.structure)
            self.car.apply()
