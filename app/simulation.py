class Simulation:

    def __init__(self, client):
        self.client = client

    def start(self):
        self.client.simxStartSimulation(self.client.simxServiceCall())

    def stop(self):
        self.client.simxStopSimulation(self.client.simxServiceCall())

    def pause(self):
        self.client.simxPauseSimulation(self.client.simxServiceCall())

    def restart(self):
        self.stop()
        self.start()

    def print(self, message):
        self.client.simxAddStatusbarMessage(message, self.client.simxDefaultPublisher())
