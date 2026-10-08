import unittest

from main import parse_args


class MainArgumentTests(unittest.TestCase):
    def test_defaults_match_simulation_configuration(self):
        args = parse_args([])

        self.assertEqual(args.floors, 5)
        self.assertEqual(args.steps, 120)
        self.assertEqual(args.initial_fire_floor, 0)
        self.assertEqual(args.ps, 0.75)
        self.assertEqual(args.ph, 0.075)
        self.assertEqual(args.combustion, 0.025)
        self.assertEqual(args.sprinkler_flow, 0)

    def test_accepts_custom_parameters(self):
        args = parse_args([
            "--floors", "3",
            "--steps", "80",
            "--initial-fire-floor", "1",
            "--ps", "0.6",
            "--ph", "0.1",
            "--combustion", "0.03",
            "--sprinkler-flow", "5",
        ])

        self.assertEqual(args.floors, 3)
        self.assertEqual(args.steps, 80)
        self.assertEqual(args.initial_fire_floor, 1)
        self.assertEqual(args.ps, 0.6)
        self.assertEqual(args.ph, 0.1)
        self.assertEqual(args.combustion, 0.03)
        self.assertEqual(args.sprinkler_flow, 5)

    def test_rejects_initial_fire_floor_outside_building(self):
        with self.assertRaises(SystemExit):
            parse_args(["--floors", "2", "--initial-fire-floor", "3"])

    def test_rejects_probability_outside_range(self):
        with self.assertRaises(SystemExit):
            parse_args(["--ps", "1.1"])


if __name__ == "__main__":
    unittest.main()
