# simulation.py

import numpy as np

from .constants import EMPTY, FIRE, IGNITION
from .propagation import burn, ignite, sprinkler
from .utils import get_cell, position
from .wind import wind_propagation


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
                for row in range(2, previous.shape[1] - 2):
                    for col in range(2, previous.shape[2] - 2):
                        cell = previous[z, row, col]
                        if cell == FIRE:
                            current[z, row, col] = burn(self.combustion)
                        elif cell == IGNITION:
                            current[z, row, col] = FIRE
                        elif cell == EMPTY and self._should_ignite(
                            previous, z, row, col
                        ):
                            current[z, row, col] = IGNITION

                if self.sprinkler_flow > 0:
                    sprinkler(current, z, self.sprinkler_flow)

            memory[t] = current

        return memory

    def _should_ignite(self, state, z, row, col):
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
            if state[z, neighbor_row, neighbor_col] != FIRE:
                continue

            opposite = direction ^ 1
            probability = self.ps * max(
                0, 1 + wind[direction] - wind[opposite]
            )
            if ignite(min(probability, 1)) == IGNITION:
                return True

        for adjacent_floor in (z - 1, z + 1):
            if (
                0 <= adjacent_floor < state.shape[0]
                and state[adjacent_floor, row, col] == FIRE
                and ignite(self.ph) == IGNITION
            ):
                return True

        return False
