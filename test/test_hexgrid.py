#!/usr/bin/env python3

import unittest
import hexgrid


class HexGridTestCase(unittest.TestCase):

    def setUp(self):
        self.hex_grid = hexgrid.HexGrid()
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

    def breadth_first_wall_filter(self, wall_hexes, hex_cell):
        if hex_cell in wall_hexes:
            return False
        return True

    def assert_breadth_first_search(self, expected_coords, calculated_results):
        for pair in zip(expected_coords, calculated_results):
            expected_hex_coords, calculated_hex_cells = pair

            expected_hex_cells = [self.hex_grid.get_cell(q, r)
                                  for q, r in expected_hex_coords]

            for calculated_hex_cell in calculated_hex_cells:
                self.assertIn(calculated_hex_cell, expected_hex_cells,
                              "Extra calculated result.")

            for expected_hex_cell in expected_hex_cells:
                self.assertIn(expected_hex_cell, calculated_hex_cells,
                              "Missing calculated result.")

    def test_breadth_first_search(self):
        origin = self.hex_grid.get_cell(0, 0)

        wall_coords = (
            (1, -1),
            (1, 0),
            (0, 1),
            (-1, 1)
        )
        wall_hexes = [hexgrid.HexCell(q, r)
                      for q, r in wall_coords]

        expected_coords = (
            (
                (-1, 0),
                (0, -1)
            ),
            (
                (-2, 1),
                (-2, 0),
                (-1, -1),
                (0, -2),
                (1, -2)
            )
        )

        bfs_filter = lambda hex_cell: \
            self.breadth_first_wall_filter(wall_hexes, hex_cell)

        self.assert_breadth_first_search(
            expected_coords,
            self.hex_grid.breadth_first_search(origin, 2, bfs_filter))

    def test_breadth_first_search_no_filter(self):
        origin = self.hex_grid.get_cell(0, 0)

        expected_coords = [
            [
                (1, 0),
                (0, 1),
                (-1, 1),
                (-1, 0),
                (0, -1),
                (1, -1)
            ]
        ]

        calculated_coords = self.hex_grid.breadth_first_search(origin, 1)
        self.assert_breadth_first_search(
            expected_coords,
            calculated_coords)

    def test_origin_neighbors(self):
        origin = self.hex_grid.get_cell(0, 0)
        neighbor_coordinates = (
            (1, -1),
            (1, 0),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (0, -1)
        )
        neighbor_hexes = [self.hex_grid.get_cell(q, r)
                          for q, r in neighbor_coordinates]

        self.assertEqual(self.hex_grid.get_neighbors(origin), neighbor_hexes)

    def test_non_origin_neighbors(self):
        center = self.hex_grid.get_cell(2, -2)
        neighbor_coordinates = (
            (3, -3),
            (3, -2),
            (2, -1),
            (1, -1),
            (1, -2),
            (2, -3)
        )
        neighbor_hexes = [self.hex_grid.get_cell(q, r)
                          for q, r in neighbor_coordinates]

        self.assertEqual(self.hex_grid.get_neighbors(center), neighbor_hexes)
