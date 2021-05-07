from api import b0RemoteApi
from car import Car
from simulation import Simulation
from controller import Controller
from meta import MetaManager
from path_finding import PathFinder

CLIENT_NAME = 'Python_client'
CHANNEL_NAME = 'b0RemoteApi'


with b0RemoteApi.RemoteApiClient(CLIENT_NAME, CHANNEL_NAME, 60) as client:
    car = Car(client)
    mm = MetaManager(client)
    simulation = Simulation(client)
    controller = Controller(car, mm)
    controller.start()
