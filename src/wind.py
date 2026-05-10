# wind.py

import numpy as np
import matplotlib.pyplot as plt

from utils import position_2d


def partial_derivative(f, i=0, h=1e-5):

    def partial(*xs):
        dxs = list(xs)
        dxs[i] += h
        return (f(*dxs) - f(*xs)) / h

    return partial


def gradient(f):

    def grad(*xs):
        return np.array([
            partial_derivative(f, i)(*xs)
            for i in range(len(xs))
        ])

    return grad


def normalize_field(field, power=1):

    a, b = field

    norm = np.sqrt(a**2 + b**2)
    max_norm = np.max(norm)

    if max_norm == 0:
        return [a, b]

    a = np.sign(a) * (np.abs(a / max_norm) ** (1 / power))
    b = np.sign(b) * (np.abs(b / max_norm) ** (1 / power))

    return [a, b]


def compute_wind_field(wind_function, domain, building, power=10):

    len_x = building.shape[2]
    len_y = building.shape[1]

    x = np.linspace(domain[0], domain[1], len_x)
    y = np.linspace(domain[2], domain[3], len_y)

    x, y = np.meshgrid(x, y)

    dx, dy = gradient(wind_function)(x, y)

    wind = [np.flipud(dx), np.flipud(dy)]

    return normalize_field(wind, power)


def wind_propagation(wind_field, coords):

    x, y, z = coords

    wx, wy = wind_field

    if not (2 <= x < wx.shape[1] - 2):
        return [0, 0, 0, 0]

    if not (2 <= y < wx.shape[0] - 2):
        return [0, 0, 0, 0]

    vx = wx[position_2d(wx, (x, y))]
    vy = wy[position_2d(wy, (x, y))]

    return [
        max(0, -vx),
        max(0, vx),
        max(0, -vy),
        max(0, vy),
    ]