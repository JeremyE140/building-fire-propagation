import argparse

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


def _non_negative_int(value):
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be an integer") from error
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return parsed


def _probability(value):
    try:
        parsed = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a number between 0 and 1") from error
    if not 0 <= parsed <= 1:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return parsed


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Simulate fire propagation in a building.")
    parser.add_argument("--floors", type=_non_negative_int, default=FLOORS,
                        help=f"number of floors above ground (default: {FLOORS})")
    parser.add_argument("--steps", type=_non_negative_int, default=SIMULATION_STEPS,
                        help=f"number of simulation steps (default: {SIMULATION_STEPS})")
    parser.add_argument(
        "--initial-fire-floor",
        type=_non_negative_int,
        default=INITIAL_FIRE_FLOOR,
        help=f"floor where the fire starts (default: {INITIAL_FIRE_FLOOR})",
    )
    parser.add_argument("--ps", type=_probability, default=0.75,
                        help="horizontal spread probability (default: 0.75)")
    parser.add_argument("--ph", type=_probability, default=0.075,
                        help="vertical spread probability (default: 0.075)")
    parser.add_argument("--combustion", type=_probability, default=0.025,
                        help="burnout probability (default: 0.025)")
    parser.add_argument("--sprinkler-flow", type=_non_negative_int, default=0,
                        help="sprinkler flow per floor and step (default: 0)")

    args = parser.parse_args(argv)
    if args.initial_fire_floor > args.floors:
        parser.error("--initial-fire-floor must be between 0 and --floors")
    return args


def main(argv=None):
    args = parse_args(argv)
    building = create_building(size=BUILDING_SIZE, floors=args.floors)
    wind_field = compute_wind_field(wind_function, WIND_DOMAIN, building)

    initial_fire = (
        BUILDING_SIZE[0] // 2,
        BUILDING_SIZE[1] // 2,
        args.initial_fire_floor,
    )
    simulation = FireSimulation(
        building,
        wind_field,
        ps=args.ps,
        ph=args.ph,
        combustion=args.combustion,
        sprinkler_flow=args.sprinkler_flow,
        initial_fire=initial_fire,
    )
    memory = simulation.run(args.steps)

    animate(memory)


if __name__ == "__main__":
    main()
