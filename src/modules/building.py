# building.py

import numpy as np

from constants import WALL, STRUCTURE, EMPTY
from utils import center


def create_building(size, floors):

    x, y = size

    building = np.full(
        (floors + 1, y + 2, x + 2),
        STRUCTURE
    )

    for z in range(floors + 1):

        building[z, 1:y + 1, 1:x + 1] = WALL
        building[z, 2:y, 2:x] = EMPTY

    return building