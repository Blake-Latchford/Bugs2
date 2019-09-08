import unittest
import math
from rules.hexcell import HexCell
from rules.hexgrid import HexGrid


class HexCellTestCase(unittest.TestCase):

    def test_equal(self):
        first = HexCell(1, 2)
        second = HexCell(1, 2)
        third = HexCell(2, 2)

        self.assertTrue(first == second)
        self.assertFalse(first == third)

    def test_not_equal(self):
        first = HexCell(1, 2)
        second = HexCell(1, 2)
        third = HexCell(2, 2)

        self.assertFalse(first != second)
        self.assertTrue(first != third)

    def test_nan_equal(self):
        first = HexCell(math.nan, math.nan)
        second = HexCell(math.nan, math.nan)

        self.assertEqual(first, second)

    def test_difference_zero(self):
        first = HexCell(0, 0)
        second = HexCell(0, 0)
        expected_result = HexCell(0, 0)

        self.assertEqual(first - second, expected_result)

    def test_difference_neighbor(self):
        first = HexCell(0, 0)
        second = HexCell(0, 1)
        expected_result = HexCell(0, -1)

        self.assertEqual(first - second, expected_result)

    def test_difference_oddball(self):
        first = HexCell(-1, 0)
        second = HexCell(1, 1)
        expected_result = HexCell(-2, -1)

        self.assertEqual(first - second, expected_result)

    def test_addition(self):
        first = HexCell(2, 0)
        second = HexCell(3, -5)
        expected_result = HexCell(5, -5)

        self.assertEqual(first + second, expected_result)

    def test_hashable(self):
        origin = HexCell(0, 0)
        non_origin = HexCell(0, 1)
        self.assertNotEqual(hash(origin), hash(non_origin))

    def test_rotate_clockwise(self):
        original = HexCell(-2, -1)
        expected_result = HexCell(-3, 2)
        calculated_result = original.rotate_clockwise_about_origin()

        self.assertEqual(expected_result, calculated_result)

    def test_rotate_counterclockwise(self):
        original = HexCell(-2, -1)
        expected_result = HexCell(1, -3)
        calculated_result = original.rotate_counterclockwise_about_origin()

        self.assertEqual(expected_result, calculated_result)

    def test_origin_neighbors(self):
        hex_grid = HexGrid()
        origin = HexCell(0, 0)
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
        hex_grid = HexGrid()
        center = HexCell(2, -2)
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
            hex_cell = HexCell(*axial)

            with self.subTest(hex_cell):
                self.assertEqual(
                    hex_cell.get_offset_coords(),
                    offset)
                self.assertEqual(
                    hex_cell,
                    HexCell.from_offset_cords(offset)
                )
