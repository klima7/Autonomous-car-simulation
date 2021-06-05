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

    driver.drive_to_path('Path29', offset=0.5, backward=False)
    driver.drive_to_path('Path32', offset=0.5, backward=True)
    # driver.drive_to_structure('StreetPaths24')
    # driver.drive_to_structure('StreetPaths9')
    # driver.drive_to_structure('RoundaboutPaths2')
    # driver.drive_to_structure('RoundaboutPaths1')
    # driver.drive_to_structure('RoundaboutPaths0')
    # driver.drive_to_structure('RoundaboutPaths3')

    while True:
        start = time()
        car.refresh()
        driver.drive()
        car.apply()
        # print(time() - start)
