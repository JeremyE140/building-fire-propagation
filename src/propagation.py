# propagation.py

import random
import numpy as np

from constants import *
from utils import *


def ignite(probability):
    return IGNITION if random.random() < probability else EMPTY


def burn(probability):
    return BURNED if random.random() < probability else FIRE


def vertical_propagation(probability):
    return IGNITION if random.random() < probability else STRUCTURE


def sprinkler(building, floor, flow):

    for _ in range(flow):

        x = random.randint(2, building.shape[2] - 3)
        y = random.randint(2, building.shape[1] - 3)

        value = get_cell(building, (x, y, floor))

        if value in [EMPTY, IGNITION, FIRE]:
            building[position(building, (x, y, floor))] = WET

        elif value == BURNED:
            building[position(building, (x, y, floor))] = BURNED_WET


def floor_on_fire(building, floor):

    return np.any(building[floor] == FIRE)