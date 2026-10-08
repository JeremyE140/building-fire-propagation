import unittest

from modules.building.generation import create_building
from modules.fire.simulation import FireSimulation
from modules.shared.constants import (
    BURNED,
    BURNED_WET,
    EMPTY,
    FIRE,
    FLAMMABLE_SURFACE,
    IGNITION,
    WALL,
    WET,
)
from modules.shared.utils import get_cell, position


class FireSimulationTests(unittest.TestCase):
    def make_building(self, floors=1):
        return create_building(size=(8, 8), floors=floors)

    def test_building_has_original_windows_corridors_and_doors(self):
        building = create_building(size=(48, 48), floors=0)

        self.assertEqual(building[0, 1, 7], EMPTY)
        self.assertEqual(building[0, 1, 20], WALL)
        self.assertEqual(building[0, 22, 10], WALL)
        self.assertEqual(building[0, 25, 10], EMPTY)
        self.assertEqual(building[0, 13, 21], EMPTY)

    def test_fire_spreads_through_window_to_outer_surface(self):
        building = create_building(size=(48, 48), floors=0)
        simulation = FireSimulation(
            building,
            wind_field=None,
            ps=1,
            ph=0,
            combustion=0,
            initial_fire=(8, 47, 0),
        )

        memory = simulation.run(3)

        self.assertEqual(get_cell(memory[1], (8, 48, 0)), IGNITION)
        self.assertEqual(get_cell(memory[2], (8, 48, 0)), FIRE)
        self.assertEqual(get_cell(memory[3], (8, 49, 0)), IGNITION)

    def test_fire_spreads_horizontally_through_empty_cells(self):
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

    def test_fire_spreads_horizontally_over_flammable_surface(self):
        building = self.make_building(floors=0)
        building[position(building, (5, 4, 0))] = FLAMMABLE_SURFACE
        simulation = FireSimulation(
            building,
            wind_field=None,
            ps=1,
            ph=0,
            combustion=0,
            initial_fire=(4, 4, 0),
        )

        memory = simulation.run(2)

        self.assertEqual(get_cell(memory[1], (5, 4, 0)), IGNITION)
        self.assertEqual(get_cell(memory[2], (5, 4, 0)), FIRE)

    def test_fire_spreads_vertically(self):
        building = self.make_building()
        building[position(building, (4, 4, 1))] = FLAMMABLE_SURFACE
        simulation = FireSimulation(
            building,
            wind_field=None,
            ps=0,
            ph=1,
            combustion=0,
            initial_fire=(4, 4, 0),
        )

        memory = simulation.run(1)

        self.assertEqual(get_cell(memory[1], (4, 4, 1)), IGNITION)

    def test_empty_does_not_ignite_vertically(self):
        simulation = FireSimulation(
            self.make_building(),
            wind_field=None,
            ps=0,
            ph=1,
            combustion=0,
            initial_fire=(4, 4, 0),
        )

        memory = simulation.run(1)

        self.assertEqual(get_cell(memory[1], (4, 4, 1)), EMPTY)

    def test_vertical_propagation_only_moves_to_the_next_floor(self):
        building = self.make_building()
        building[position(building, (4, 4, 0))] = FLAMMABLE_SURFACE
        simulation = FireSimulation(
            building,
            wind_field=None,
            ps=0,
            ph=1,
            combustion=0,
            initial_fire=(4, 4, 1),
        )

        memory = simulation.run(1)

        self.assertEqual(get_cell(memory[1], (4, 4, 0)), FLAMMABLE_SURFACE)

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

    def test_wet_cells_dry_back_to_their_original_state(self):
        building = self.make_building(floors=0)
        building[position(building, (5, 4, 0))] = WET
        building[position(building, (6, 4, 0))] = BURNED_WET
        simulation = FireSimulation(
            building,
            wind_field=None,
            ps=0,
            ph=0,
            combustion=0,
            initial_fire=(4, 4, 0),
        )

        memory = simulation.run(1)

        self.assertEqual(get_cell(memory[1], (5, 4, 0)), EMPTY)
        self.assertEqual(get_cell(memory[1], (6, 4, 0)), BURNED)

    def test_sprinkler_only_runs_on_floors_with_active_fire(self):
        from unittest.mock import patch

        building = self.make_building()
        simulation = FireSimulation(
            building,
            wind_field=None,
            ps=0,
            ph=0,
            combustion=0,
            sprinkler_flow=1,
            initial_fire=(4, 4, 0),
        )

        with patch("modules.fire.propagation.random.randint", return_value=3):
            memory = simulation.run(1)

        self.assertEqual(get_cell(memory[1], (3, 3, 1)), EMPTY)


if __name__ == "__main__":
    unittest.main()
