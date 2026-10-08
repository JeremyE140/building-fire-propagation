# building.py

import numpy as np

from ..shared.constants import WALL, FLAMMABLE_SURFACE, EMPTY
from ..shared.utils import center


def create_building(size, floors):
    x, y = size

    building = np.full(
        (floors + 1, y + 2, x + 2),
        FLAMMABLE_SURFACE
    )

    for z in range(floors + 1):

        building[z, 1:y + 1, 1:x + 1] = WALL
        building[z, 2:y, 2:x] = EMPTY

    _add_windows(building)
    _add_corridors(building)
    _add_doors(building)

    return building


def _add_windows(building):
    wall_x = building.shape[2] - 4
    wall_y = building.shape[1] - 4
    window_x = int(wall_x / 8)
    window_y = int(wall_y / 8)

    for floor in range(building.shape[0]):
        building[floor, 1, window_x + 2:2 * window_x + 2] = EMPTY
        building[floor, 1, 6 * window_x + 2:7 * window_x + 2] = EMPTY
        building[floor, wall_y + 2, window_x + 2:2 * window_x + 2] = EMPTY
        building[floor, wall_y + 2, 6 * window_x + 2:7 * window_x + 2] = EMPTY
        building[floor, window_y + 2:2 * window_y + 2, 1] = EMPTY
        building[floor, 6 * window_y + 2:7 * window_y + 2, 1] = EMPTY
        building[floor, window_y + 2:2 * window_y + 2, wall_x + 2] = EMPTY
        building[floor, 6 * window_y + 2:7 * window_y + 2, wall_x + 2] = EMPTY


def _add_corridors(building):
    wall_x = building.shape[2] - 4
    wall_y = building.shape[1] - 4
    half_window_x = int(wall_x / 16)
    half_window_y = int(wall_y / 16)
    x, y = center(building)

    for floor in range(building.shape[0]):
        building[floor, y - half_window_y - 1, 1:wall_x + 3] = WALL
        building[floor, y + half_window_y + 1, 1:wall_x + 3] = WALL
        building[
            floor,
            y - half_window_y - 1,
            x - half_window_x:x + half_window_x + 1,
        ] = EMPTY
        building[
            floor,
            y + half_window_y + 1,
            x - half_window_x:x + half_window_x + 1,
        ] = EMPTY

        building[floor, 1:wall_y + 3, x - half_window_x - 1] = WALL
        building[floor, 1:wall_y + 3, x + half_window_x + 1] = WALL
        building[
            floor,
            y - half_window_y:y + half_window_y + 1,
            x - half_window_x - 1,
        ] = EMPTY
        building[
            floor,
            y - half_window_y:y + half_window_y + 1,
            x + half_window_x + 1,
        ] = EMPTY


def _add_doors(building):
    wall_x = building.shape[2] - 4
    wall_y = building.shape[1] - 4
    half_wall_x = int(wall_x / 4)
    half_wall_y = int(wall_y / 4)
    half_window_x = int(wall_x / 16)
    half_window_y = int(wall_y / 16)
    x, y = center(building)

    door_centers = (
        (x - half_window_x - 1, y + half_wall_y),
        (x + half_wall_x, y + half_window_y + 1),
        (x - half_wall_x, y - half_window_y - 1),
        (x + half_window_x + 1, y - half_wall_y),
    )

    for floor in range(building.shape[0]):
        for door_x, door_y in door_centers:
            row = building.shape[1] - 1 - door_y
            building[floor, row - 1:row + 2, door_x - 1:door_x + 2] = EMPTY