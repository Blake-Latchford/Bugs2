#!/usr/bin/env python3

import unittest
import hexcell
import hexgrid


class HexCellTestCase(unittest.TestCase):

    def test_equal(self):
        first = hexcell.HexCell(1, 2)
        second = hexcell.HexCell(1, 2)
        third = hexcell.HexCell(2, 2)

        self.assertTrue(first == second)
        self.assertFalse(first == third)

    def test_not_equal(self):
        first = hexcell.HexCell(1, 2)
        second = hexcell.HexCell(1, 2)
        third = hexcell.HexCell(2, 2)

        self.assertFalse(first != second)
        self.assertTrue(first != third)

    def test_hashable(self):
        origin = hexcell.HexCell(0, 0)
        non_origin = hexcell.HexCell(0, 1)
        self.assertNotEqual(hash(origin), hash(non_origin))

    def test_distance_origin_to_origin(self):
        origin = hexcell.HexCell(0, 0)
        self.assertEqual(origin.distance(origin), 0)

    def test_distance_offset_from_origin(self):
        first = hexcell.HexCell(-1, -1)
        second = hexcell.HexCell(0, 2)
        self.assertEqual(first.distance(second), 4)

    def test_origin_neighbors(self):
        hex_grid = hexgrid.HexGrid()
        origin = hexcell.HexCell(0, 0)
        neighbor_coordinates = (
            (1, -1),
            (1, 0),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (0, -1)
        )
        neighbor_hexes = [hex_grid.get_cell(q, r)
                          for q, r in neighbor_coordinates]

        self.assertEqual(origin.get_neighbors(hex_grid), neighbor_hexes)

    def test_non_origin_neighbors(self):
        hex_grid = hexgrid.HexGrid()
        center = hexcell.HexCell(2, -2)
        neighbor_coordinates = (
            (3, -3),
            (3, -2),
            (2, -1),
            (1, -1),
            (1, -2),
            (2, -3)
        )
        neighbor_hexes = [hex_grid.get_cell(q, r)
                          for q, r in neighbor_coordinates]

        self.assertEqual(center.get_neighbors(hex_grid), neighbor_hexes)


if __name__ == "__main__":
    unittest.main()
