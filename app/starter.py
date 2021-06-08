from api import b0RemoteApi
from car import Car
from meta import MetaManager
from driving import Driver
from time import time

CLIENT_NAME = 'Python_client'
CHANNEL_NAME = 'b0RemoteApi'


with b0RemoteApi.RemoteApiClient(CLIENT_NAME, CHANNEL_NAME, inactivityToleranceInSec=60, timeout=10) as client:
    car = Car(client)
    mm = MetaManager(client)
    driver = Driver(car, mm)

    # Parking
    driver.drive_to_path('Path197', offset=0.7)
    driver.drive_to_path('Path192', offset=0.1, backward=True)
    driver.drive_to_path('Path170', offset=0.5)

    # Reversing
    driver.drive_to_path('Path29', offset=0.1)
    driver.drive_to_path('Path4', offset=0.1, backward=True)
    driver.drive_to_path('Path41', offset=0.5)

    # Driving forward to some streets
    driver.drive_to_structure('StreetPaths9')
    driver.drive_to_structure('RoundaboutPaths0')

    # Drive backward to some streets
    driver.drive_to_structure('StreetPaths9', backward=True)
    driver.drive_to_structure('RoundaboutPaths0', backward=True)

    while True:
        start = time()
        car.refresh()
        driver.update()
        car.apply()
        # print(time() - start)
