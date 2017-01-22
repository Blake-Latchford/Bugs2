import unittest
import hexcell
import hexgrid
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
