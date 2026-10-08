# simulation.py

import numpy as np

from ..environment.wind import wind_propagation
from ..shared.constants import (
    BURNED,
    BURNED_WET,
    EMPTY,
    FIRE,
    FLAMMABLE_SURFACE,
    IGNITION,
    WET,
)
from ..shared.utils import get_cell, position
from .propagation import burn, floor_on_fire, ignite, sprinkler


class FireSimulation:

    def __init__(
        self,
        building,
        wind_field,
        ps=0.75,
        ph=0.075,
        combustion=0.025,
        sprinkler_flow=0,
        initial_fire=None,
    ):

        self.building = np.array(building, copy=True)
        self.wind_field = wind_field

        self.ps = ps
        self.ph = ph
        self.combustion = combustion
        self.sprinkler_flow = sprinkler_flow

        if initial_fire is None:
            initial_fire = (
                self.building.shape[2] // 2,
                self.building.shape[1] // 2,
                0,
            )

        x, y, z = initial_fire
        if not (
            0 <= z < self.building.shape[0]
            and 0 <= x < self.building.shape[2]
            and 0 <= y < self.building.shape[1]
        ):
            raise ValueError("initial_fire coordinates are outside the building")
        if get_cell(self.building, initial_fire) != EMPTY:
            raise ValueError("initial_fire must point to an empty cell")
        self.building[position(self.building, (x, y, z))] = FIRE

    def run(self, steps):
        if steps < 0:
            raise ValueError("steps must be non-negative")

        memory = np.empty((steps + 1, *self.building.shape), dtype=self.building.dtype)
        memory[0] = self.building

        for t in range(1, steps + 1):
            previous = memory[t - 1]
            current = previous.copy()

            for z in range(previous.shape[0]):
                for row in range(previous.shape[1]):
                    for col in range(previous.shape[2]):
                        cell = previous[z, row, col]
                        if cell == FIRE:
                            current[z, row, col] = burn(self.combustion)
                        elif cell == IGNITION:
                            current[z, row, col] = FIRE
                        elif cell == WET:
                            current[z, row, col] = EMPTY
                        elif cell == BURNED_WET:
                            current[z, row, col] = BURNED
                        elif cell in (EMPTY, FLAMMABLE_SURFACE) and self._should_ignite(
                            previous, z, row, col, cell
                        ):
                            current[z, row, col] = IGNITION

                if self.sprinkler_flow > 0 and floor_on_fire(current, z):
                    sprinkler(current, z, self.sprinkler_flow)

            memory[t] = current

        return memory

    def _should_ignite(self, state, z, row, col, cell):
        x = col
        y = state.shape[1] - 1 - row
        wind = (
            wind_propagation(self.wind_field, (x, y, z))
            if self.wind_field is not None
            else [0, 0, 0, 0]
        )

        neighbors = (
            (row, col - 1, 0),
            (row, col + 1, 1),
            (row + 1, col, 2),
            (row - 1, col, 3),
        )
        for neighbor_row, neighbor_col, direction in neighbors:
            if not (
                0 <= neighbor_row < state.shape[1]
                and 0 <= neighbor_col < state.shape[2]
            ):
                continue
            if state[z, neighbor_row, neighbor_col] != FIRE:
                continue

            opposite = direction ^ 1
            probability = self.ps * max(
                0, 1 + wind[direction] - wind[opposite]
            )
            if ignite(min(probability, 1)) == IGNITION:
                return True

        if (
            cell == FLAMMABLE_SURFACE
            and z > 0
            and state[z - 1, row, col] == FIRE
            and ignite(self.ph) == IGNITION
        ):
            return True

        return False
