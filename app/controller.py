class Controller:

    def __init__(self, car, mm):
        self.car = car
        self.mm = mm

    def start(self):

        # Hardcoded starting point
        path = [p for p in self.mm.paths if p.handle == 1071][0]
        print(path, path.structure)

        while True:
            self.car.refresh()
            self.car.navigate(self.car.target_point)
            if self.car.target_point[0] == path.end.x and self.car.target_point[1] == path.end.y:
                path = path.successors[0]
                self.car.cur_path = path.handle
                print(path, path.structure)
            self.car.apply()
