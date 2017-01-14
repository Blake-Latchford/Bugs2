#!/usr/bin/env python3

import unittest
import hexcell
import hexgrid

class HexCellTestCase(unittest.TestCase):
    
    def setUp(self):
        self.hex_grid = hexgrid.HexGrid()
    
    def test_equal(self):
        first = hexcell.HexCell(self.hex_grid, 1, 2)
        second = hexcell.HexCell(self.hex_grid, 1, 2)
        third = hexcell.HexCell(self.hex_grid, 2, 2)

        self.assertTrue(first == second)
        self.assertFalse(first == third)

    def test_not_equal(self):
        first = hexcell.HexCell(self.hex_grid, 1, 2)
        second = hexcell.HexCell(self.hex_grid, 1, 2)
        third = hexcell.HexCell(self.hex_grid, 2, 2)

        self.assertFalse(first != second)
        self.assertTrue(first != third)


    def breadth_first_wall_filter(self, wall_hexes, hex_cell):
        if hex_cell in wall_hexes:
            return False
        return True


    def test_breadth_first_search(self):
        origin = hexcell.HexCell(self.hex_grid, 0, 0)

        wall_coords = (
            ( 1, -1 ),
            ( 1, 0 ),
            ( 0, 1 ),
            ( -1, 1 )
        )
        wall_hexes = [ hexcell.HexCell(self.hex_grid, q, r)
            for q, r in wall_coords ]

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

        bfs_filter = lambda hex_cell: \
            self.breadth_first_wall_filter(wall_hexes, hex_cell)

        calculated_results = origin.breadth_first_search(2, bfs_filter)
        for distance, calculated_hex_cells in enumerate(calculated_results):
            expected_hex_cells = [hexcell.HexCell(self.hex_grid, q, r)
                                  for q, r in expected_coords[distance]]
            
            for calculated_hex_cell in calculated_hex_cells:
                self.assertIn(calculated_hex_cell, expected_hex_cells,
                              "Extra calculated result.")
                
            for expected_hex_cell in expected_hex_cells:
                self.assertIn(expected_hex_cell, calculated_hex_cells,
                              "Missing calculated result.")
    
    def test_hashable(self):
        origin = hexcell.HexCell(self.hex_grid, 0, 0)
        non_origin = hexcell.HexCell(self.hex_grid, 0, 1)
        self.assertNotEqual(hash(origin), hash(non_origin))

    def test_origin_neighbors(self):
        origin = hexcell.HexCell(self.hex_grid, 0, 0)
        neighbor_coordinates = (
            ( 1, -1 ),
            ( 1, 0 ),
            ( 0, 1 ),
            ( -1, 1 ),
            ( -1, 0 ),
            ( 0, -1 )
        )
        neighbor_hexes = [ hexcell.HexCell(self.hex_grid, q, r)
                          for q, r in neighbor_coordinates ]

        self.assertEqual(origin.get_neighbors(), neighbor_hexes)

    def test_non_origin_neighbors(self):
        center = hexcell.HexCell(self.hex_grid, 2, -2)
        neighbor_coordinates = (
            ( 3, -3 ),
            ( 3, -2 ),
            ( 2, -1 ),
            ( 1, -1 ),
            ( 1, -2 ),
            ( 2, -3 )
        )
        neighbor_hexes = [ hexcell.HexCell(self.hex_grid, q, r)
                          for q, r in neighbor_coordinates ]

        self.assertEqual(center.get_neighbors(), neighbor_hexes)
        
    def test_distance_origin_to_origin(self):
        origin = hexcell.HexCell(self.hex_grid, 0, 0)
        self.assertEqual(origin.distance(origin), 0)

    def test_distance_offset_from_origin(self):
        first = hexcell.HexCell(self.hex_grid, -1, -1)
        second = hexcell.HexCell(self.hex_grid, 0, 2)
        self.assertEqual(first.distance(second), 4)

if __name__ == "__main__":
    unittest.main()
