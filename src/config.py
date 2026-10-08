BUILDING_SIZE = (48, 48)
FLOORS = 5
WIND_DOMAIN = (-1, 1, -1, 1)
SIMULATION_STEPS = 120
INITIAL_FIRE_FLOOR = 0


def wind_function(x, y):
    return (x**2 + y**2) ** 0.5
