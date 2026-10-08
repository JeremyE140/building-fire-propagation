from config import (
    BUILDING_SIZE,
    FLOORS,
    INITIAL_FIRE_FLOOR,
    SIMULATION_STEPS,
    WIND_DOMAIN,
    wind_function,
)
from modules.building.generation import create_building
from modules.environment.wind import compute_wind_field
from modules.fire.simulation import FireSimulation
from modules.visualization.rendering import animate


def main():
    building = create_building(size=BUILDING_SIZE, floors=FLOORS)
    wind_field = compute_wind_field(wind_function, WIND_DOMAIN, building)

    initial_fire = (
        BUILDING_SIZE[0] // 2,
        BUILDING_SIZE[1] // 2,
        INITIAL_FIRE_FLOOR,
    )
    simulation = FireSimulation(building, wind_field, initial_fire=initial_fire)
    memory = simulation.run(SIMULATION_STEPS)

    animate(memory)


if __name__ == "__main__":
    main()
