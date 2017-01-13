#!/usr/bin/env python3

import unittest
import hexgrid

class DirectionTestCase(unittest.TestCase):

    def test_basic_clockwise(self):
        self.assertEqual(
            hexgrid.Direction.S_POS.next_clockwise(),
            hexgrid.Direction.Q_NEG)

    def test_wrap_clockwise(self):
        self.assertEqual(
            hexgrid.Direction.S_NEG.next_clockwise(),
            hexgrid.Direction.Q_POS)

    def test_basic_counterclockwise(self):
        self.assertEqual(
            hexgrid.Direction.Q_NEG.next_counterclockwise(),
            hexgrid.Direction.S_POS)

    def test_wrap_counterclockwise(self):
        self.assertEqual(
            hexgrid.Direction.Q_POS.next_counterclockwise(),
            hexgrid.Direction.S_NEG)

class HexCellTestCase(unittest.TestCase):
    
    def test_equal(self):
        hex_grid = hexgrid.HexGrid()
        first = HexCell(hex_grid, 1, 2)
        second = HexCell(hex_grid, 1, 2)
        third = HexCell(hex_grid, 2, 2)

        self.assertTrue(first == second)
        self.assertFalse(first == third)

    def test_not_equal(self):
        hex_grid = hexgrid.HexGrid()
        first = HexCell(hex_grid, 1, 2)
        second = HexCell(hex_grid, 1, 2)
        third = HexCell(hex_grid, 2, 2)

        self.assertFalse(first != second)
        self.assertTrue(first != third)

    def test_origin_neighbors(self):
        hex_grid = hexgrid.HexGrid()
        neighbor_coordinates = (
            ( 1, -1 ),
            ( 1, 0 ),
            ( 0, 1 ),
            ( -1, 1 ),
            ( -1, 0 ),
            ( 0, -1 )
        )
        

if __name__ == "__main__":
    unittest.main()
