import unittest

from modules.building import create_building
from modules.constants import BURNED, EMPTY, FIRE, IGNITION
from modules.simulation import FireSimulation
from modules.utils import get_cell


class FireSimulationTests(unittest.TestCase):
    def make_building(self, floors=1):
        return create_building(size=(8, 8), floors=floors)

    def test_fire_spreads_horizontally(self):
        building = self.make_building(floors=0)
        simulation = FireSimulation(
            building,
            wind_field=None,
            ps=1,
            ph=0,
            combustion=0,
            initial_fire=(4, 4, 0),
        )

        memory = simulation.run(2)

        self.assertEqual(get_cell(memory[0], (4, 4, 0)), FIRE)
        self.assertEqual(get_cell(memory[1], (5, 4, 0)), IGNITION)
        self.assertEqual(get_cell(memory[2], (5, 4, 0)), FIRE)
        self.assertEqual(get_cell(building, (4, 4, 0)), EMPTY)

    def test_fire_spreads_vertically(self):
        simulation = FireSimulation(
            self.make_building(),
            wind_field=None,
            ps=0,
            ph=1,
            combustion=0,
            initial_fire=(4, 4, 0),
        )

        memory = simulation.run(1)

        self.assertEqual(get_cell(memory[1], (4, 4, 1)), IGNITION)

    def test_fire_burns_out(self):
        simulation = FireSimulation(
            self.make_building(floors=0),
            wind_field=None,
            ps=0,
            ph=0,
            combustion=1,
            initial_fire=(4, 4, 0),
        )

        memory = simulation.run(1)

        self.assertEqual(get_cell(memory[1], (4, 4, 0)), BURNED)


if __name__ == "__main__":
    unittest.main()
