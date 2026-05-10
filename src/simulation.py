# simulation.py

import numpy as np

from propagation import *
from constants import *


class FireSimulation:

    def __init__(
        self,
        building,
        wind_field,
        ps=0.75,
        ph=0.075,
        combustion=0.025,
        sprinkler_flow=0,
    ):

        self.building = building
        self.wind_field = wind_field

        self.ps = ps
        self.ph = ph
        self.combustion = combustion
        self.sprinkler_flow = sprinkler_flow

    def run(self, steps):

        memory = np.zeros(
            (steps + 1, *self.building.shape)
        )

        memory[0] = self.building.copy()

        for t in range(1, steps + 1):

            # future propagation ici
            memory[t] = self.building.copy()

        return memory