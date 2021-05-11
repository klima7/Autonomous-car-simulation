from pathfinder import PathFinder


class Controller:

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm

    def start(self):

        # Hardcoded start and end point
        start = [p for p in self.mm.paths if p.handle == 1071][0]
        end = [p for p in self.mm.paths if p.handle == 1266][0]

        navigator = PathFinder()
        paths_ahead = navigator.find_path(start, end)

        path = start
        print(path, path.structure)

        while True:
            self.car.refresh()
            self.car.navigate(self.car.target_point)
            if self.car.target_point[0] == path.end.x and self.car.target_point[1] == path.end.y:
                path = paths_ahead[0]
                paths_ahead = paths_ahead[1:]
                self.car.cur_path = path.handle
                print(path, path.structure)
            self.car.apply()
