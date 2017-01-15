#!/usr/bin/env python3

import unittest
import hexcell


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

if __name__ == "__main__":
    unittest.main()
