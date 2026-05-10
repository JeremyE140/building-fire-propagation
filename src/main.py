# main.py

from building import create_building
from wind import compute_wind_field
from simulation import FireSimulation
from rendering import animate


def wind_function(x, y):
    return (x**2 + y**2) ** 0.5


building = create_building(
    size=(48, 48),
    floors=5
)

wind_field = compute_wind_field(
    wind_function,
    [-1, 1, -1, 1],
    building
)

simulation = FireSimulation(
    building,
    wind_field
)

memory = simulation.run(120)

animate(memory)