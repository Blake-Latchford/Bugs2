import unittest
from rules.hexgrid import HexGrid


class HexGridTestCase(unittest.TestCase):

    def setUp(self):
        self.hex_grid = HexGrid()
        self.origin_cell = self.hex_grid.get_cell(0, 0)
        self.hex_grid.register_cell(self.origin_cell)

    def test_find_registered_cell(self):
        self.assertIs(
            self.hex_grid.get_cell(0, 0),
            self.origin_cell)

    def test_dont_find_registered_cell(self):
        first_unregistered_cell = self.hex_grid.get_cell(0, 1)
        second_unregistered_cell = self.hex_grid.get_cell(0, 1)

        self.assertEqual(first_unregistered_cell, second_unregistered_cell)
        self.assertIsNot(first_unregistered_cell, second_unregistered_cell)

    def test_unregister_cell(self):
        hex_cell = self.hex_grid.get_cell(0, 1)
        self.hex_grid.register_cell(hex_cell)
        self.hex_grid.unregister_cell(hex_cell)
        self.assertIsNot(
            self.hex_grid.get_cell(hex_cell.q, hex_cell.r),
            hex_cell)

    def test_reset(self):
        hex_cell = self.hex_grid.get_cell(0, 1)
        self.hex_grid.register_cell(hex_cell)
        self.hex_grid.reset()

        self.assertIsNot(hex_cell, self.hex_grid.get_cell(0, 1))
