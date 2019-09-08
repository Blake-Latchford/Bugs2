import unittest
import rules.hexcell as hexcell
import rules.hexgrid as hexgrid
import math


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

    def test_nan_equal(self):
        first = hexcell.HexCell(math.nan, math.nan)
        second = hexcell.HexCell(math.nan, math.nan)

        self.assertEqual(first, second)

    def test_difference_zero(self):
        first = hexcell.HexCell(0, 0)
        second = hexcell.HexCell(0, 0)
        expected_result = hexcell.HexCell(0, 0)

        self.assertEqual(first - second, expected_result)

    def test_difference_neighbor(self):
        first = hexcell.HexCell(0, 0)
        second = hexcell.HexCell(0, 1)
        expected_result = hexcell.HexCell(0, -1)

        self.assertEqual(first - second, expected_result)

    def test_difference_oddball(self):
        first = hexcell.HexCell(-1, 0)
        second = hexcell.HexCell(1, 1)
        expected_result = hexcell.HexCell(-2, -1)

        self.assertEqual(first - second, expected_result)

    def test_addition(self):
        first = hexcell.HexCell(2, 0)
        second = hexcell.HexCell(3, -5)
        expected_result = hexcell.HexCell(5, -5)

        self.assertEqual(first + second, expected_result)

    def test_hashable(self):
        origin = hexcell.HexCell(0, 0)
        non_origin = hexcell.HexCell(0, 1)
        self.assertNotEqual(hash(origin), hash(non_origin))

    def test_rotate_clockwise(self):
        original = hexcell.HexCell(-2, -1)
        expected_result = hexcell.HexCell(-3, 2)
        calculated_result = original.rotate_clockwise_about_origin()

        self.assertEqual(expected_result, calculated_result)

    def test_rotate_counterclockwise(self):
        original = hexcell.HexCell(-2, -1)
        expected_result = hexcell.HexCell(1, -3)
        calculated_result = original.rotate_counterclockwise_about_origin()

        self.assertEqual(expected_result, calculated_result)

    def test_origin_neighbors(self):
        hex_grid = hexgrid.HexGrid()
        origin = hexcell.HexCell(0, 0)
        expected_neighbors = (
            (1, -1),
            (1, 0),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (0, -1)
        )

        neighbors = list(origin.get_neighbors(hex_grid))

        for neighbor_coordinate in expected_neighbors:
            with self.subTest(neighbor_coordinate):
                cell = hex_grid.get_cell(*neighbor_coordinate)
                self.assertIn(cell, neighbors)

    def test_non_origin_neighbors(self):
        hex_grid = hexgrid.HexGrid()
        center = hexcell.HexCell(2, -2)
        expected_neighbors = (
            (3, -3),
            (3, -2),
            (2, -1),
            (1, -1),
            (1, -2),
            (2, -3)
        )

        neighbors = list(center.get_neighbors(hex_grid))

        for neighbor_coordinate in expected_neighbors:
            with self.subTest(neighbor_coordinate):
                cell = hex_grid.get_cell(*neighbor_coordinate)
                self.assertIn(cell, neighbors)

    def test_get_offset_cords(self):
        equivalent_coords = (
            ((0, 0), (0, 0)),
            ((7, 0), (7, 0)),
            ((-15, 0), (-15, 0)),
            ((-1, 2), (0, 2)),
            ((1, -2), (0, -2)),
            ((1, 2), (2, 2)),
            ((-1, -2), (-2, -2)),
            ((-3, 2), (-2, +2)),
            ((3, -2), (2, -2)),
            ((2, -2), (1, -2)),
        )

        for axial, offset in equivalent_coords:
            hex_cell = hexcell.HexCell(*axial)

            with self.subTest(hex_cell):
                self.assertEqual(
                    hex_cell.get_offset_coords(),
                    offset)
                self.assertEqual(
                    hex_cell,
                    hexcell.HexCell.from_offset_cords(offset)
                )
