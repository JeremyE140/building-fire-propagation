# utils.py

import numpy as np


def position(building, coords):
    x, y, z = coords
    y = (building.shape[1] - 1) - y
    return z, y, x


def position_2d(array, coords):
    x, y = coords
    y = (array.shape[0] - 1) - y
    return y, x


def get_cell(building, coords):
    return building[position(building, coords)]


def center(building):
    x = building.shape[2] // 2
    y = building.shape[1] // 2
    return x, y


def neighbors(building, coords):
    x, y, z = coords

    neigh = []

    if x > 0:
        neigh.append((x - 1, y, z))

    if x < building.shape[2] - 1:
        neigh.append((x + 1, y, z))

    if y > 0:
        neigh.append((x, y - 1, z))

    if y < building.shape[1] - 1:
        neigh.append((x, y + 1, z))

    return neigh