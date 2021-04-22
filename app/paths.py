from api.b0RemoteApi import RemoteApiClient


class Path:

    def __init__(self, client: RemoteApiClient, path_handle):
        self._client = client

        self.handle = path_handle
        _, self.length = self._client.simxGetPathLength(self.handle, self._client.simxServiceCall())
        _, self.start = self._client.simxGetPositionOnPath(self.handle, 1, self._client.simxServiceCall())
        _, self.end = self._client.simxGetPositionOnPath(self.handle, 0, self._client.simxServiceCall())


class PathsManager:

    PARENT_NAME = 'RoadPaths'
    ACCEPTABLE_POINTS_DISTANCE = 0.001

    def __init__(self, client: RemoteApiClient):
        self._client = client
        self._paths_map = self._create_map()

    def _create_map(self):
        paths = self._fetch_paths()
        paths_map = {}
        for p1 in paths:
            p1_successors = []
            for p2 in paths:
                if p2 is p1:
                    continue
                if PathsManager._is_path_subsequent(p1, p2):
                    p1_successors.append(p2)
            paths_map[p1.handle] = p1_successors
        return paths_map

    def _fetch_paths(self):
        _, parent_handle = self._client.simxGetObjectHandle(PathsManager.PARENT_NAME, self._client.simxServiceCall())
        _, paths_handles = self._client.simxGetObjectsInTree(parent_handle, "sim.handle_all", 1, self._client.simxServiceCall())

        paths = []

        for path_handle in paths_handles:
            path = Path(self._client, path_handle)
            paths.append(path)

        return paths

    @staticmethod
    def _is_path_subsequent(first_path, subsequent_path):
        return abs(first_path.end[0] - subsequent_path.start[0]) < PathsManager.ACCEPTABLE_POINTS_DISTANCE and \
               abs(first_path.end[1] - subsequent_path.start[1]) < PathsManager.ACCEPTABLE_POINTS_DISTANCE

    def find_subsequent_paths(self, path):
        return self._paths_map[path.handle]


