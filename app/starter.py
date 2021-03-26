from api import b0RemoteApi
from simulation import Simulation
from car import Car
from controller import Controller


CLIENT_NAME = 'Python_client'
CHANNEL_NAME = 'b0RemoteApi'


with b0RemoteApi.RemoteApiClient(CLIENT_NAME, CHANNEL_NAME, 60) as client:

    try:
        simulation = Simulation(client)
        car = Car(client)
        controller = Controller(simulation, car)
        print("width = ", car.width)
        print("length = ", car.length)
        simulation.restart()
        controller.start()
    finally:
        simulation.stop()
