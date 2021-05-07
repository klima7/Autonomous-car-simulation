class Temp:
    def __init__(self, path):
        self.this = path
        self.neighbors = []
        self.prev = None
        #self.create_neighbors()

    def create_neighbors(self):
        for successor in self.this.successors:
            t = Temp(successor)
            t.prev = self
            self.neighbors.append(t)


class PathFinder:
    def __init__(self, start, end):
        self.start = Temp(start)
        self.end = end
        self.routes = self.find_routes()
        self.shortest = self.find_shortest_route()
        self.shortest_way = self.create_shortest_way()

    def find_routes(self):
        open_list = []
        closed_list = []
        routes = []
        open_list.append(self.start)
        while len(open_list) > 0:
            x = open_list.pop(0)
            if self.check_if_end(x.this):
                routes.append(x)
                continue
            closed_list.append(x)
            for neighbor in x.this.successors:
                if self.check_if_in_closed(neighbor, closed_list):
                    continue
                else:
                    t = Temp(neighbor)
                    t.prev = x
                    open_list.append(t)

        return routes

    def check_if_end(self, p):
        return self.end.handle == p.handle

    def check_if_in_closed(self, p, closed):
        for item in closed:
            if item.this.handle == p.handle:
                return True

        return False

    def find_route_length(self, route):
        length = 0
        r = route.prev
        while True:
            if r is None:
                return length
            length += r.this.length
            r = r.prev

    def find_shortest_route(self):
        min = self.find_route_length(self.routes[0])
        min_route = self.routes[0]
        for route in self.routes:
            length = self.find_route_length(route)
            if length < min:
                min = length
                min_route = route

        return min_route

    def create_shortest_way(self):
        arr = []
        r = self.shortest
        while True:
            if r.prev is None:
                return arr.reverse()

            arr.append(r.this)
            r = r.prev
