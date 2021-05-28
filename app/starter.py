from api import b0RemoteApi
from car import Car
from meta import MetaManager
from driving import Driver

CLIENT_NAME = 'Python_client'
CHANNEL_NAME = 'b0RemoteApi'


with b0RemoteApi.RemoteApiClient(CLIENT_NAME, CHANNEL_NAME, inactivityToleranceInSec=60, timeout=10) as client:
    car = Car(client)
    mm = MetaManager(client)
    driver = Driver(car, mm)

    driver.add_target('RoundaboutPaths2')
    driver.add_target('RoundaboutPaths1')
    driver.add_target('RoundaboutPaths0')
    driver.add_target('RoundaboutPaths3')

    while True:
        car.refresh()
        driver.drive()
        car.apply()
