# Autonomous car simulation
Simulation of autonomous car with CoppeliaSim Robot Simulator and Python.

# Car
<img src="https://github.com/klima7/Autonomous-car-simulation/blob/images/images/car.jpg" width="500" />

## Sensors
- Camera (512 x 256 px)
- GPS
- Compass
- 6 distance sensors
- Lidar

## Executive systems
- Ackerman steering
- Position lamps
- Stop lights
- Reversing lights
- Avaryune lights
- Turn signals

# Map
Simplified, but huge map with building, pavements, parkings and so on. The car is able to follow a predetermined route between a series of specified points, even backwards. Algorithm A* has been used to find shortest path.

<img src="https://github.com/klima7/Autonomous-car-simulation/blob/images/images/map.jpg" width="500" />

# Crossings
Standard crossings and roundabouts. Car is able to move properly through each of them. The car correctly lets off the turn signals when it passes through.

<img src="https://github.com/klima7/Autonomous-car-simulation/blob/images/images/crossings.jpg" width="700" />

# Signs
Standard signs and traffic lights. Car is recognizing them with neural network and reacting for some of them.

<img src="https://github.com/klima7/Autonomous-car-simulation/blob/images/images/signs.jpg" width="700" />

# Starting
- Install Python dependencies with `pip install -r requirements.txt`
- Use Coppelia Sim 4.1.0

# Authors
- Łukasz Klimkiewicz ([klima7](https://github.com/klima7))
- Mateusz Majewski ([majewskimateusz](https://github.com/majewskimateusz))
- Mikołaj Imbor ([1mbir](https://github.com/1mbir))

