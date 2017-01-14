#!/usr/bin/env python3

from hexcell import HexCell

class HexGrid:
    def __init__(self):
        self.populated_cells = {}

    def get_cell(self, q, r):
        coords = (q, r)
        if coords in self.populated_cells:
            return self.populated_cells[coords]
        return HexCell(self, q, r)