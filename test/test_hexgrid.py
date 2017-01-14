#!/usr/bin/env python3

import unittest
import hexgrid

class HexGridTestCase(unittest.TestCase):
    
    def setUp(self):
        self.hex_grid = hexgrid.HexGrid()