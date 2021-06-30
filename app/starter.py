import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}


from api import b0RemoteApi
from car import Car
from meta import MetaManager
from driving import Driver
from time import time


CLIENT_NAME = 'Python_client'
CHANNEL_NAME = 'b0RemoteApi'


with b0RemoteApi.RemoteApiClient(CLIENT_NAME, CHANNEL_NAME, inactivityToleranceInSec=60, timeout=30) as client:
    car = Car(client)
    mm = MetaManager(client)
    driver = Driver(car, mm)

    driver.drive_to_path('Path172', offset=0.9)
    driver.drive_to_path('Path194', offset=0.3)
    driver.drive_to_path('Path192', offset=0.15, backward=True)

    driver.drive_to_path('Path163', offset=0.05)
    driver.drive_to_path('Path155', offset=0.05, backward=True)
    driver.drive_to_path('Path209', offset=0.5)

    while True:
        start = time()
        car.refresh()
        driver.update()
        car.apply()
        # print(time() - start, car.orient)
