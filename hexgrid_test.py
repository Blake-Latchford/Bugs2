#!/usr/bin/env python3

import unittest
import hexgrid

class HexCellTestCase(unittest.TestCase):
    
    def test_equal(self):
        hex_grid = hexgrid.HexGrid()
        first = hexgrid.HexCell(hex_grid, 1, 2)
        second = hexgrid.HexCell(hex_grid, 1, 2)
        third = hexgrid.HexCell(hex_grid, 2, 2)

        self.assertTrue(first == second)
        self.assertFalse(first == third)

    def test_not_equal(self):
        hex_grid = hexgrid.HexGrid()
        first = hexgrid.HexCell(hex_grid, 1, 2)
        second = hexgrid.HexCell(hex_grid, 1, 2)
        third = hexgrid.HexCell(hex_grid, 2, 2)

        self.assertFalse(first != second)
        self.assertTrue(first != third)

    def test_origin_neighbors(self):
        hex_grid = hexgrid.HexGrid()
        origin = hexgrid.HexCell(hex_grid, 0, 0)
        neighbor_coordinates = (
            ( 1, -1 ),
            ( 1, 0 ),
            ( 0, 1 ),
            ( -1, 1 ),
            ( -1, 0 ),
            ( 0, -1 )
        )
        neighbor_hexes = [ hexgrid.HexCell(hex_grid, q, r) for q, r in neighbor_coordinates ]

        self.assertEqual(origin.get_neighbors(), neighbor_hexes)

    def test_non_origin_neighbors(self):
        hex_grid = hexgrid.HexGrid()
        center = hexgrid.HexCell(hex_grid, 2, -2)
        neighbor_coordinates = (
            ( 3, -3 ),
            ( 3, -2 ),
            ( 2, -1 ),
            ( 1, -1 ),
            ( 1, -2 ),
            ( 2, -3 )
        )
        neighbor_hexes = [ hexgrid.HexCell(hex_grid, q, r) for q, r in neighbor_coordinates ]

        self.assertEqual(center.get_neighbors(), neighbor_hexes)
        
    def test_distance_origin_to_origin(self):
        hex_grid = hexgrid.HexGrid()
        origin = hexgrid.HexCell(hex_grid, 0, 0)
        self.assertEqual(origin.distance(origin), 0)

    def test_distance_offset_from_origin(self):
        hex_grid = hexgrid.HexGrid()
        first = hexgrid.HexCell(hex_grid, -1, -1)
        second = hexgrid.HexCell(hex_grid, 0, 2)
        self.assertEqual(first.distance(second), 4)

    def breadth_first_wall_filter(self, wall_hexes, hex_cell):
        if hex_cell in wall_hexes:
            return False
        return True


    def test_breadth_first_search(self):
        hex_grid = hexgrid.HexGrid()
        origin = hexgrid.HexCell(hex_grid, 0, 0)

        wall_coords = (
            ( 1, -1 ),
            ( 1, 0 ),
            ( 0, 1 ),
            ( -1, 1 )
        )
        wall_hexes = [ hexgrid.HexCell(hex_grid, q, r) for q, r in wall_coords ]

        expected_coords = (
            (
                ( -1, 0 ),
                ( 0, -1 )
            ),
            (
                ( -2, 1 ),
                ( -2, 0 ),
                ( -1, -1 ),
                ( 0, -2 ),
                ( 1, -2 )
            )
        )

        bfs_filter = lambda hex_cell: self.breadth_first_wall_filter(wall_coords, hex_cell)

        calculated_results = origin.breadth_first_search(2, bfs_filter)

        for distance, calculated_hex_cells in enumerate(calculated_results):
            expected_hex_cells = [hexgrid.HexCell(hex_grid, q, r) for q, r in expected_coords[distance]]
            self.assertEqual(len(calculated_hex_cells), len(expected_hex_cells))


if __name__ == "__main__":
    unittest.main()
