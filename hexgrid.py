#!/usr/bin/env python3

from hexcell import HexCell

class HexGrid:
    def __init__(self):
        self._populated_cells = {}

    def get_cell(self, q, r):
        """Get the cell at the specified coordinates. If no cell is registered
        at that location, create a temporary new cell."""
        
        coords = (q, r)
        if coords in self._populated_cells:
            return self._populated_cells[coords]
        return HexCell(self, q, r)
    
    def register_cell(self, hex_cell):
        """Register a hex cell to be retained in the grid."""
        
        self._populated_cells[(hex_cell.q, hex_cell.r)] = hex_cell